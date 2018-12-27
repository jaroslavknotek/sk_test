import unittest
from unittest.mock import patch
import src.carcounter as cc


class CarCounterTestCase(unittest.TestCase):
    def test_countcars(self):
        carcounter = cc.CarCounter({"id": None, "user": None, "pass": None}, [])

        with patch('utils.decode_content') as mock:
            mock.return_value= {
                "features": [{
                    "properties": {
                        "class": "cars",
                        "count": 1
                    }
                },
                    {
                        "properties": {
                            "class": "cars",
                            "count": 5
                        }
                    },
                    {
                        "properties": {
                            "class": "notcars",
                            "count": 12
                        }
                    }

                ]
            }

            assert carcounter.count_cars([""]) == 6

    def test_countcars_invalid_json(self):
        carcounter = cc.CarCounter({"id": None, "user": None, "pass": None}, [])

        with patch('utils.decode_content') as mock:
            mock.return_value= {
                "features": [{
                    "invalid_properties": {
                        "class": "cars",
                        "count": 1
                    }
                }

                ]
            }

            assert carcounter.count_cars([""]) == 0


if __name__ == '__main__':
    unittest.main()
