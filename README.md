# AI-Fun-Winter-Camp

## Arkanoid_GamePass

在 [arkanoid.py](https://github.com/Jesse-Jumbo/AI-Fun-Winter-Camp/blob/main/arkanoid.py) 寫 rule 玩遊戲蒐集資料，蒐集的資料會存在 [log](https://github.com/Jesse-Jumbo/AI-Fun-Winter-Camp/tree/main/log) 裡面，

- 注意：
  - Arkanoid 內的球移動反彈後，是全完全反射
  - 資料蒐集愈多樣性愈好，可以透過：
    1. 不同的發球方向（預設往左）
    2. 自製不同的地圖關卡遊玩
    3. 在不同的地方發球（預設原地）
    4. 透過 platform 的左右邊緣，製造切球
    
將收集來的資料，透過 [model_1.py](https://github.com/Jesse-Jumbo/AI-Fun-Winter-Camp/blob/main/model_1.py) ，整理特徵格式，確認每個 feature 相應的 標籤（label）

- 注意：
  - 使用 regression 訓練時，label 為預測的落點
  - 使用 classification 時，label 則為板子移動的方向
  
### 回歸

將資料拆成 8:2 的訓練及測試，使用 decision tree 回歸器訓練，評估指標及樹深的參數調整

最後將訓練好的 model 存在 [save](https://github.com/Jesse-Jumbo/AI-Fun-Winter-Camp/tree/main/save)

### 分類

一樣將資料拆成 8:2 的訓練及測試，使用 KNN 分類器，找到最好的 k 值，使得 Accuracy（被分對資料的比例）最大（1.0）

然後一樣在最後，將訓練好的 model 存在 [save](https://github.com/Jesse-Jumbo/AI-Fun-Winter-Camp/tree/main/save)

## 遊戲破關

以 [autoplay.py](https://github.com/Jesse-Jumbo/AI-Fun-Winter-Camp/blob/main/autoplay.py) 啟動遊戲遊玩

### init 初始化

選擇在 [save](https://github.com/Jesse-Jumbo/AI-Fun-Winter-Camp/tree/main/save) 裡的模型載入

### updata 更新

根據訓練好的 model 預測出的 label 來移動板子（程式碼的架構，就類似於蒐集遊戲資料的程式 [arkanoid.py](https://github.com/Jesse-Jumbo/AI-Fun-Winter-Camp/blob/main/arkanoid.py) ）
