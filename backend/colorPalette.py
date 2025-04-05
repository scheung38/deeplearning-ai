class ColorPalette:
    def __init__(self, colors):
        self.colors = colors

class DefaultColorPalette(ColorPalette):
    def __init__(self):
        super().__init__(["#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f1c40f", "#1abc9c"])

class BrightColorPalette(ColorPalette):
    def __init__(self):
        super().__init__(["#2980b9", "#e67e73", "#8bc34a", "#e5e5e5", "#ffc107", "#4caf50"])

class PastelColorPalette(ColorPalette):
    def __init__(self):
        super().__init__(["#4567b7", "#ffb3b3", "#a3d5f3", "#d6e9f2", "#ffd7be", "#c9e4ca"])
