import json


class Size:
    # Converts sizes to the right format
    def __init__(self, sku, name):
        self.sku = sku
        self.name = name

    def get_size(self, size):
        json_file = open("converters/sizes.json")
        sizes = json.load(json_file)

        if 'GSB' in self.sku or 'BB' in self.sku:
            if 'BBW' in self.sku:
                sizes['BBW'][size]
            else:
                try:
                    size = size.replace(' 2E', '')
                except:
                    pass
                return sizes['New_balance'][size]
        elif '(W)' in self.name:
            if 'UGG' in self.name:
                return sizes['UGG'][size]
            else:
                return sizes['W'][size]
        elif 'C' in size or 'TD' in self.name:
            return sizes['C'][size]
        elif 'adidas' in self.name:
            return sizes['Adidas'][size]
        else:
            return sizes['M'][size]
