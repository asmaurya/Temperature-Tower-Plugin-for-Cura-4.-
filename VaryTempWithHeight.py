# Created by AbhishekSinghMaurya @2019
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

from typing import List

from ..Script import Script

#  Performs a search-and-replace on all g-code.
class VaryTempWithHeight(Script):
    def getSettingDataString(self):
        return """{
            "name": "Vary Temp with Height",
            "key": "VaryTempWithHeight",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "change_at":
                {
                    "label": "Change Temp at",
                    "description": "Whether to decrease temp at layer or height interval",
                    "type": "enum",
                    "options": {"height": "Height", "layer": "Layer No."},
                    "default_value": "layer"
                },
                "height_inc":
                {
                    "label": "Height Interval",
                    "description": "At the increase of how many mm height does the temp decreases",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 5.0,
                    "minimum_value": 0,
                    "minimum_value_warning": "0.27",
                    "enabled": "change_at == 'height'"
                },
                "layer_inc": 
                {
                    "label": "Layer Interval",
                    "description": "At the increase of how many layers does the temp decreases",
                    "type": "int",
                    "value": 1,
                    "minimum_value": 0,
                    "minimum_value_warning": "1",
                    "enabled": "change_at == 'layer'"
                },
                "layer_start": 
                {
                    "label": "Start Layer",
                    "description": "From which layer the temp decrease to be started",
                    "type": "int",
                    "value": 1,
                    "minimum_value": 0,
                    "minimum_value_warning": "1"
                },
                "temperature_start":
                {
                    "label": "Start Temperature",
                    "description": "Initial nozzle temperature",
                    "unit": "°C",
                    "type": "int",
                    "default_value": 200
                },
                "temperature_inc":
                {
                    "label": "Temperature Decrement Step",
                    "description": "Decrease temperature by this much with each height increment",
                    "unit": "°C",
                    "type": "int",
                    "default_value": 5
                }
            }
        }"""

    #\param data A list of layers of g-code.
    def execute(self, data: List[str]):
        selection_value=self.getSettingValueByKey("change_at")
        if selection_value == "layer":
            layer_inc_value = self.getSettingValueByKey("layer_inc")
        start_temp_value = self.getSettingValueByKey("temperature_start")
        start_layer_value = self.getSettingValueByKey("layer_start")
        temp_inc_value = self.getSettingValueByKey("temperature_inc")
        new_temp = start_temp_value + temp_inc_value
        prepend_gcode = ""
        #prepend_gcode += ";added code by post processing\n"
        #prepend_gcode += ";script: varytempwithheight.py\n"
        for current_layer in range(start_layer_value, len(data)-2, layer_inc_value):
            new_temp -= temp_inc_value
            if new_temp < 0:
                new_temp = 0
            prepend_gcode = "\nM104 S" + str(new_temp) + "  ; Added by VaryTempWithHeight Prost processing plugin by ASM \n"
            #data[current_layer] = prepend_gcode + data[current_layer]
            data[current_layer] = data[current_layer] + prepend_gcode
            #return data
        return data
