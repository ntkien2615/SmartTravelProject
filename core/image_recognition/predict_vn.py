import os
import io
import torch
from torchvision import models, transforms
from PIL import Image

# Determine the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "model_vietnam.pth")
CLASSES_PATH = os.path.join(CURRENT_DIR, "classes.txt")

class ImagePredictor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImagePredictor, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"ImagePredictor initializing on device: {self.device}")

        # Load Class Names
        if not os.path.exists(CLASSES_PATH):
            raise FileNotFoundError(f"Classes file not found at {CLASSES_PATH}")
        
        with open(CLASSES_PATH, "r", encoding="utf-8") as f:
            self.class_names = [line.strip() for line in f.readlines()]
        
        self.num_classes = len(self.class_names)

        # Load Model
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

        self.model = models.resnet18(weights=None)
        in_features = self.model.fc.in_features
        self.model.fc = torch.nn.Linear(in_features, self.num_classes)

        state_dict = torch.load(MODEL_PATH, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()
        self.model.to(self.device)

        # Preprocessing
        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

    def _predict_tensor(self, img_tensor: torch.Tensor):
        with torch.no_grad():
            outputs = self.model(img_tensor)
            probs = torch.softmax(outputs, dim=1)
            conf, pred_idx = torch.max(probs, 1)
            pred_idx = pred_idx.item()
            conf = conf.item()

        label = self.class_names[pred_idx]
        return label, conf

    def predict_pil_image(self, img: Image.Image):
        """Dự đoán từ PIL Image (dùng cho Streamlit)."""
        img = img.convert("RGB")
        tensor = self.preprocess(img).unsqueeze(0).to(self.device)
        return self._predict_tensor(tensor)

    def predict_image_bytes(self, image_bytes: bytes):
        """Dự đoán từ bytes ảnh."""
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.preprocess(img).unsqueeze(0).to(self.device)
        return self._predict_tensor(tensor)

# Singleton instance accessor
def get_predictor():
    return ImagePredictor()
