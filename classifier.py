import tensorflow as tf
import numpy as np
import tarfile
import os
import math
from PIL import Image
import datetime
import matplotlib

# object detection utils
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import ops as utils_ops


class Classifier:
    def __init__(self):
        PATH_TO_FROZEN_GRAPH = os.path.abspath(
            './model/frozen_inference_graph.pb')
        PATH_TO_LABELS = os.path.abspath('./model/labelmap.pbtxt')

        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        self.category_index = label_map_util.create_category_index_from_labelmap(
            PATH_TO_LABELS)
        self.graph = detection_graph

    def run_inference(self, image):
        with self.graph.as_default():
            with tf.Session() as sess:
                # Get handles to input and output tensors
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {
                    output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph(
                        ).get_tensor_by_name(tensor_name)
                if 'detection_masks' in tensor_dict:
                    # The following processing is only for single image
                    detection_boxes = tf.squeeze(
                        tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(
                        tensor_dict['detection_masks'], [0])
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(
                        tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [
                                               real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [
                                               real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[0], image.shape[1])
                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict,
                                       feed_dict={image_tensor: np.expand_dims(image, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(
                    output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(
                    np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]
        return output_dict

    def detect(self, image, coordinates, min_confidence=0.8):
        """ """
        image_np = load_image_into_numpy_array(image)
        (im_width, im_height) = image.size

        output_dict = self.run_inference(image_np)
        boxes = output_dict["detection_boxes"]
        classes = output_dict["detection_classes"]
        scores = output_dict['detection_scores']
        detections = []
        for i in range(output_dict['num_detections']):
            if (scores[i] >= min_confidence):
                detections.append({
                    'box': box_to_pixel(im_width, im_height, boxes[i]),
                    'label': self.lookup_class(classes[i]),
                    'confidence': scores[i].item(),
                    'coordinates': coordinates
                })
        self.save_image(image_np, output_dict)
        return detections

    def lookup_class(self, class_id):
        return self.category_index[class_id]['name']

    def save_image(self, image_np, output_dict):
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            self.category_index,
            instance_masks=output_dict.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=3)
        img = Image.fromarray(image_np)
        name = "classified_{}.jpg".format(datetime.datetime.now())
        img.save(name)


def box_to_pixel(width, height, coordinates):
    ymin, xmin, ymax, xmax = coordinates
    coordinates = [height * ymin, width * xmin, height * ymax, width * xmax]
    return {
        'ymin': math.floor(ymin * height),
        'xmin': math.floor(xmin * width),
        'ymax': math.floor(ymax * height),
        'xmax': math.floor(xmax * width)
    }


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)
