# Copyright (c) 2017 Ruben Dulek
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

from typing import List

from ..Script import Script

##  Performs a search-and-replace on all g-code.
#
#   Due to technical limitations, the search can't cross the border between
#   layers.
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
        # for index, layer in enumerate(data):
        #     lines = layer.split("\n")
        #     #Scroll each line of instruction for each layer in the G-code
        #     for line in lines:
        #         # first positive layer reached
        #         if ";layer:0" in line:
        #             layers_started = true
        #         # count nbr of negative layers (raft)
        #         elif ";layer:-" in line:
        #             nbr_negative_layers += 1
        #         if not layers_started:
        #             continue

        #         # if a z instruction is in the line, read the current z
        #         if self.getvalue(line, "z") is not none:
        #             current_z = self.getvalue(line, "z")

        #         if selection_value == "height":
        #             # ignore if the line is not g1 or g0
        #             if self.getvalue(line, "g") != 1 and self.getvalue(line, "g") != 0:
        #                 continue

        #             # this block is executed once, the first time there is a g
        #             # command, to get the z offset (z for first positive layer)
        #             if not got_first_g_cmd_on_layer_0:
        #                 layer_0_z = current_z - initial_layer_height
        #                 got_first_g_cmd_on_layer_0 = true

        #             current_height = current_z - layer_0_z
        #             if (current_height % height_inc) > layer_height:  #####
        #                 continue  #you have got the correct layer 

        #         # decrease at layer
        #         else:
        #             if not line.startswith(";layer:"):
        #                 continue
        #             current_layer = line[len(";layer:"):]
        #             try:
        #                 current_layer = int(current_layer)

        #             # couldn't cast to int. something is wrong with this
        #             # g-code data
        #             except valueerror:
        #                 continue
        #             if (current_layer % layer_inc) !=0:
        #                 continue

        #         prepend_gcode = ";type:custom\n"
        #         prepend_gcode += ";added code by post processing\n"
        #         prepend_gcode += ";script: varytempwithheight.py\n"
        #         new_temp = temperature_start
        #         if selection_value == "height":
        #             prepend_gcode += ";current z: {z}\n".format(z = current_z)
        #             prepend_gcode += ";current height: {height}\n".format(height = current_height)
        #             new_temp -= int(current_z / height_inc) * temp_inc
        #         else:
        #             prepend_gcode += ";current layer: {layer}\n".format(layer = current_layer)
        #             new_temp -= int(current_layer / layer_inc) * temp_inc
        #         # set extruder temperature
        #         prepend_gcode += self.putvalue(m = 104, s = new_temp) + "; new temperature\n"
        #         # prepend_gcode +=  "\n m104 s" + new_temp + " ; new temperature\n"
               
        #         layer = prepend_gcode + layer
        #         #layer = layer+'\n ;asm'

        #         # override the data of this layer with the
        #         # modified data
        #         data[index] = layer
        #         return data
        # return data