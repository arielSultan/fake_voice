from nakdimon_ort import Nakdimon 

nakdimon = Nakdimon("nakdimon.onnx")

def add_niqqud(text):
    dotted_text = nakdimon.compute(text)
    return dotted_text
