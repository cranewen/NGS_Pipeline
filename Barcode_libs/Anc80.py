
class Anc80:
    def __init__(self):
        self.lib_name = "Anc80BC_"

        self.barcode_dict = \
        {
            'B1_AAA': 0, 'B1_AGA': 1,
            'B2_GCA': 0, 'B2_TCA': 1,
            'B3_GCA': 0, 'B3_GGA': 1,
            'B4_AAA': 0, 'B4_AGA': 1,
            'B5_CAG': 0, 'B5_GAG': 1,
            'B6_ACG': 0, 'B6_GAG': 1,
            'B7_ACG': 0, 'B7_GCG': 1,
            'B8_AAT': 0, 'B8_AGT': 1,
            'B9_CAG': 0, 'B9_GAG': 1,
            'B10_GCA': 0, 'B10_TCA': 1,
            'B11_AAC': 0, 'B11_GAC': 1}

        self.barcode_array = \
            ['B1', 'B2', 'B3', \
             'B4', 'B5', 'B6', \
             'B7', 'B8', 'B9', \
             'B10', 'B11']

