import unittest
import src
import io
import numpy as np
import src.utils as utils
from PIL import Image


class UtilsTestCase(unittest.TestCase):
    def test_order2d_2x2(self):
        data = [((2, 1), "tr"), ((1, 2), "bl"), ((2, 2), "br"), ((1, 1), "tl")]
        expected = [
            [((1, 1), "tl"), ((2, 1), "tr")],
            [((1, 2), "bl"), ((2, 2), "br")]
        ]

        ordered = utils.order_2d(data)
        self.assertEqual(ordered, expected)

    def test_order2d_2x3(self):
        data = [((2, 1), "tr"), ((1, 2), "bl"), ((2, 2), "br"), ((1, 1), "tl"), ((1, 3), "xx"), ((2, 3), "yy")]
        expected = [
            [((1, 1), "tl"), ((2, 1), "tr")],
            [((1, 2), "bl"), ((2, 2), "br")],
            [((1, 3), "xx"), ((2, 3), "yy")]
        ]

        ordered = utils.order_2d(data)
        self.assertEqual(ordered, expected)

    def test_construct_image(self):
        image1_tr = Image.fromarray(np.zeros((3, 3)))
        image1_tl = Image.fromarray(np.ones((3, 3)))
        image1_br = Image.fromarray(np.full((3, 3),2))
        image1_bl = Image.fromarray(np.full((3, 3),3))

        data = [((2, 1), image1_tr), ((1, 2), image1_bl), ((2, 2), image1_br), ((1, 1), image1_tl)]
        image = utils.construct_image(data)
        ar = np.asarray(image).min(axis=2)
        # top left
        result =ar[:3,:3].astype(np.uint8)
        expected=np.ones((3,3)).astype(np.uint8)
        self.assertTrue(np.array_equal(result,expected))
        # top right
        result = ar[:3, 3:].astype(np.uint8)
        expected = np.zeros((3, 3)).astype(np.uint8)
        self.assertTrue(np.array_equal(result, expected))

        #bottom left
        result = ar[3:, :3].astype(np.uint8)
        expected = np.full((3, 3),3).astype(np.uint8)
        self.assertTrue(np.array_equal(result, expected))

        # bottom right
        result = ar[3:, 3:].astype(np.uint8)
        expected = np.full((3, 3),2).astype(np.uint8)
        self.assertTrue(np.array_equal(result, expected))


if __name__ == '__main__':
    unittest.main()
