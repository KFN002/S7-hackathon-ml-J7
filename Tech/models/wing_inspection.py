import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import torch.nn as nn

class WingInspectionModel(nn.Module):
    def __init__(self):
        super(WingInspectionModel, self).__init__()
        self.model = models.resnet50(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, 3)  # 3 класса: [1 - OK, 2 - странно, 3 - критично]

    def forward(self, x):
        return self.model(x)

    def predict(self, img):
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        img = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = self.forward(img)
            prediction = torch.argmax(output, dim=1).item()
        labels = {0: "Все в порядке", 1: "Есть подозрительные зоны", 2: "Критическое обледенение!"}
        return labels[prediction], prediction + 1
