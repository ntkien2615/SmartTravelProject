## Sơ Đồ train.py và predict_vn.py
## Tổng quan 
```mermaid
flowchart TD
    %% ===== KHỐI DỮ LIỆU =====
    A["Thu thập ảnh địa điểm ở Việt Nam"] --> B["Tổ chức thư mục\n dataset/train và dataset/val\nmỗi lớp 1 folder"]

    %% ===== GIAI ĐOẠN HUẤN LUYỆN =====
    subgraph G1["Giai đoạn huấn luyện (train.py)"]
        B --> C["Đọc cấu hình\nbatch size, số epoch, learning rate"]
        C --> D["Tạo ImageFolder\ntrain_dataset, val_dataset"]
        D --> E["Khởi tạo ResNet18\nthay lớp cuối theo số lớp"]
        E --> F["Vòng lặp huấn luyện + kiểm tra\ntrain loop + val loop"]
        F --> G["Chọn model tốt nhất\ntheo accuracy trên val"]
        G --> H["Lưu model_vietnam.pth\nvà classes.txt"]
    end

    %% ===== GIAI ĐOẠN SỬ DỤNG (BACKEND + FRONTEND) =====
    subgraph G2["Giai đoạn sử dụng (backend + giao diện)"]
        H --> I["backend_model.py\nload model_vietnam.pth\nvà classes.txt"]
        I --> J["Frontend (Streamlit / Tkinter)\nimport backend_model"]
        J --> K["Người dùng upload ảnh\nhoặc chọn file ảnh"]
        K --> L["Frontend gọi hàm\npredict_image_path / predict_pil_image"]
        L --> M["Backend tiền xử lý ảnh\nResize, Normalize, tạo tensor"]
        M --> N["Model dự đoán\nsoftmax để lấy xác suất"]
        N --> O["Trả về nhãn địa điểm\nvà độ tin cậy cho frontend"]
        O --> P["Hiển thị kết quả cho người dùng\n(ví dụ: 'cho_ben_thanh 95%')"]
    end

    A:::dataNode
    B:::dataNode
    classDef dataNode fill:#eef,stroke:#333;
```
## khởi tạo & gọi hàm train_model.
```mermaid
flowchart TD
    A["Start\nChạy train.py"] --> B["Thiết lập hằng số\nDATA_DIR, BATCH_SIZE, NUM_EPOCHS, ..."]
    B --> C["Định nghĩa transforms\ntrain_transform, val_transform"]
    C --> D["Tạo ImageFolder\ntrain_dataset, val_dataset"]
    D --> E["Tạo DataLoader\ntrain_loader, val_loader"]
    E --> F["Lấy class_names\nvà num_classes"]
    F --> G["Ghi class_names ra\nclasses.txt"]
    G --> H["Khởi tạo ResNet18\n(pretrained ImageNet)"]
    H --> I["Thay fc bằng Linear mới\nnum_classes"]
    I --> J["Đưa model lên DEVICE\n(CPU/GPU)"]
    J --> K["Tạo loss function\nCrossEntropyLoss"]
    K --> L["Tạo optimizer Adam\nlr = LR"]
    L --> M["Tạo scheduler\nReduceLROnPlateau"]
    M --> N["Gọi train_model(NUM_EPOCHS)"]
    N --> O["Kết thúc chương trình"]
```
## hàm train_model.
```mermaid
flowchart TD
    A["Start\ntrain_model(num_epochs)"] --> B["Khởi tạo\nbest_acc = 0\nepochs_no_improve = 0"]
    B --> C["epoch = 1"]
    C --> D{"epoch ≤ num_epochs\nvà chưa early stop?"}
    D -->|Không| E["In best_acc & best_epoch\nreturn"]
    D -->|Có| F["Train 1 epoch\n(train loop)"]
    F --> G["Tính train_loss\nvà train_acc"]
    G --> H["Validate 1 epoch\n(val loop)"]
    H --> I["Tính val_loss\nvà val_acc"]
    I --> J["scheduler.step(val_loss)"]
    J --> K{"val_acc > best_acc?"}
    K -->|Có| L["Cập nhật best_acc\nlưu model_vietnam.pth\nreset epochs_no_improve = 0"]
    K -->|Không| M["epochs_no_improve += 1"]
    L --> N
    M --> N{"epochs_no_improve ≥ PATIENCE?"}
    N -->|Có| E
    N -->|Không| O["epoch += 1"] --> D
```
## train loop
```mermaid
flowchart TD
    A["Start\nTrain loop 1 epoch"] --> B["model.train()"]
    B --> C["Khởi tạo\nrunning_loss = 0\nrunning_corrects = 0\ntotal = 0"]
    C --> D{{"Lặp qua từng batch\ntrong train_loader"}}
    D -->|Còn batch| E["Chuyển inputs, labels\nlên DEVICE"]
    E --> F["optimizer.zero_grad()"]
    F --> G["outputs = model(inputs)"]
    G --> H["loss = criterion(outputs, labels)"]
    H --> I["preds = argmax(outputs)"]
    I --> J["loss.backward()"]
    J --> K["optimizer.step()"]
    K --> L["Cộng dồn\nrunning_loss, running_corrects, total"]
    L --> D
    D -->|Hết batch| M["train_loss = running_loss / total\ntrain_acc = running_corrects / total"]
    M --> N["Kết thúc train loop\ntrả về train_loss, train_acc"]
```
## val loop
```mermaid
flowchart TD
    A["Start\nVal loop 1 epoch"] --> B["model.eval()"]
    B --> C["Khởi tạo\nval_loss = 0\nval_corrects = 0\nval_total = 0"]
    C --> D{{"Lặp qua từng batch\ntrong val_loader"}}
    D -->|Còn batch| E["Chuyển inputs, labels\nlên DEVICE"]
    E --> F["Chạy trong no_grad\n(ko tính gradient)"]
    F --> G["outputs = model(inputs)"]
    G --> H["loss = criterion(outputs, labels)"]
    H --> I["preds = argmax(outputs)"]
    I --> J["Cộng dồn\nval_loss, val_corrects, val_total"]
    J --> D
    D -->|Hết batch| K["val_loss = val_loss / val_total\nval_acc = val_corrects / val_total"]
    K --> L["Kết thúc val loop\ntrả về val_loss, val_acc"]
```
## Sơ đồ predict_vn.py
## hàm core_predict_tensor_topk
```mermaid
flowchart TD
    A["Start\n_predict_tensor_topk(img_tensor, k)"] --> B["Nhận img_tensor\nshape [1,3,224,224]\n(đã preprocess, trên DEVICE)"]
    B --> C["outputs = model(img_tensor)"]
    C --> D["probs = softmax(outputs, dim=1)"]
    D --> E["Giới hạn k ≤ num_classes"]
    E --> F["Lấy top-k:\nconfs, idxs = topk(probs, k)"]
    F --> G["Chuyển về list Python\nconfs, idxs"]
    G --> H["Tạo list kết quả\nfor (i,c) → (CLASS_NAMES[i], c)"]
    H --> I["Trả về\n[(label1, conf1), ..., (labelk, confk)]"]
```
## hàm predict_image_path
```mermaid 
flowchart TD
    A["Start\npredict_image_path(image_path)"] --> B["Image.open(image_path)"]
    B --> C["Chuyển sang RGB\nimg.convert('RGB')"]
    C --> D["tensor = preprocess(img)"]
    D --> E["tensor = tensor.unsqueeze(0)\n[1,3,224,224]"]
    E --> F["tensor.to(DEVICE)"]
    F --> G["Gọi _predict_tensor_topk(tensor, k=1)"]
    G --> H["Nhận top1 = (label, confidence)"]
    H --> I["Trả về (label, confidence)\ncho frontend (hoặc main)"]
```

## hàm predict_pil_image và predict_image_bytes
```mermaid 
flowchart TD
    A["Start\npredict_pil_image(img)"] --> B["img.convert('RGB')"]
    B --> C["tensor = preprocess(img)"]
    C --> D["tensor = tensor.unsqueeze(0)\n[1,3,224,224]"]
    D --> E["tensor.to(DEVICE)"]
    E --> F["Gọi _predict_tensor_topk(tensor, k=1)"]
    F --> G["Trả về (label, confidence)"]

    %% NHÁNH BYTES
    H["Start\npredict_image_bytes(image_bytes)"] --> I["Tạo img = Image.open(io.BytesIO(image_bytes))"]
    I --> J["img.convert('RGB')"]
    J --> K["tensor = preprocess(img)"]
    K --> L["tensor = tensor.unsqueeze(0)\n[1,3,224,224]"]
    L --> M["tensor.to(DEVICE)"]
    M --> N["Gọi _predict_tensor_topk(tensor, k=1)"]
    N --> O["Trả về (label, confidence)"]
```
## hàm predict_topk_*
```mermaid 
flowchart TD
    A["Start\n__main__ trong backend_model.py"] --> B["Đọc sys.argv\nimage_path, k (nếu có)"]
    B --> C{"Có image_path hợp lệ?"}
    C -->|Không| D["In hướng dẫn sử dụng\npython backend_model.py path/to/img.jpg [k]"] --> Z["End"]
    C -->|Có| E["Gọi predict_topk_image_path(image_path, k)"]
    E --> F["predict_topk_image_path:\nload ảnh → preprocess → _predict_tensor_topk(tensor, k)"]
    F --> G["Nhận list\n[(label1, conf1), ..., (labelk, confk)]"]
    G --> H["In từng dòng\nlabel + độ tin cậy %"]
    H --> Z["End"]
```