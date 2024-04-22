# soft_computing 
**TOC**
- [soft\_computing](#soft_computing)
- [Swarm Algorithm](#swarm-algorithm)
    - [測試優化程序效率的函數](#測試優化程序效率的函數)
  - [PSO (Particle Swarm Optimization)](#pso-particle-swarm-optimization)
    - [速度更新公式](#速度更新公式)
    - [PSO Psuedo Code](#pso-psuedo-code)
  - [ABC (Artificial Bee Colony)](#abc-artificial-bee-colony)
    - [ABC Psuedo Code](#abc-psuedo-code)
  - [ACO (Ant Colony Optimization)](#aco-ant-colony-optimization)
    - [轉移規則](#轉移規則)
    - [ACO Psuedo Code](#aco-psuedo-code)
  - [FireFly](#firefly)
  - [GA (Genetic Algorithm)](#ga-genetic-algorithm)
---
# Swarm Algorithm
Swarm Algorithm (群智算法)   
可以手打一個演算法或是使用`pyswarms`函示庫獲得相關演算法。  
Swarm Algorithm是一種透過模仿自然界生物的群體行為的計算方式，透過模擬社會動物(螞蟻、鳥等)來解決複雜的優化問題，核心思想是透過個體之間的簡單規則和相互作用來尋找全局最優解(Global Optimize)。

---
### 測試優化程序效率的函數
1. Rastrigin Function
$$ f(\mathbf{x}) = An + \sum_{i=1}^n \left[x_i^2 - A \cos(2\pi x_i)\right] $$
- \( A \) is usually set to 10.
- \( n \) is the dimensionality of the problem.
2. Styblinski-Tang Function
$$ f(\mathbf{x}) = \frac{1}{2} \sum_{i=1}^n \left(x_i^4 - 16x_i^2 + 5x_i\right) $$
- \( n \) is the dimensionality of the problem.
---
<details>
<summary>PSO (Particle Swarm Optimization)</summary>

## PSO (Particle Swarm Optimization)
* 適用於非凸或導數難以計算的優化問題  
* 每個粒子(Particle)都有一個初始的位置以及速度，速度影響的是移動的方向和距離。  

### 速度更新公式
```python
vi = w * vi + c1 * rand() * (pbest_i - xi) + c2 * rand() * (gbest - xi)
```
從公式中可以看到粒子保留一部分前一次的速度`w * vi`，並且朝向個體最佳解`pbest`以及全體最佳解`gbest`前進
* 透過算好的速度更新位置  

[PSO程式碼](./PSO.py)  
### PSO Psuedo Code
```md
初始化：
1. 初始化粒子群的數量 N。
2. 對於每個粒子 i，隨機初始化位置 xi 和速度 vi。
3. 設定每個粒子的個體最佳位置（pbest）為其初始位置。
4. 設定全局最佳位置（gbest）為具有最佳適應度值的粒子的位置。
5. 對於每個粒子 i：
   a. 計算粒子的適應度值 f(xi)。
   b. 如果 f(xi) 優於該粒子的 pbest 的適應度值，則更新 pbest 為當前位置 xi。
   c. 如果 f(xi) 優於 gbest 的適應度值，則更新 gbest 為當前位置 xi。

6. 對於每個粒子 i：
   a. 更新速度 vi 依據以下公式：
      vi = w * vi + c1 * rand() * (pbest_i - xi) + c2 * rand() * (gbest - xi)
   b. 更新位置 xi 依據以下公式：
      xi = xi + vi

   其中：
   - w 是慣性權重，控制前一速度對當前速度的影響。
   - c1 和 c2 是學習因子，通常 c1 是個體學習因子，c2 是社會學習因子。
   - rand() 是一個生成[0,1]範圍內隨機數的函數。

7. 檢查終止條件（例如迭代次數或解的質量）。

輸出：
8. 輸出全局最佳位置 gbest 和對應的最佳適應度值。
```
</details>

<details>
<summary>ABC (Artificial Bee Colony)</summary>

## ABC (Artificial Bee Colony)
在ABC演算法中蜜蜂被分成三種角色
1. 僱傭蜂（Employed bees）
   * 每個僱傭蜂負責一個特定的食物來源(local解)
   * 探索食物來源附近區域的食物品質(解的好壞) -> 決定是否要在食物來源附近找新的食物
2. 觀察蜂（Onlooker bees）
   * 等待**僱傭蜂（Employed bees）** 傳回的信息選擇比較好的食物來源品質進行搜索
3. 偵察蜂（Scout bees）
   * 如果一個食物來源被認為不值得探索時，雇傭蜂會變成偵查蜂，**隨機**尋找新的食物來源  

[ABC程式碼](./ABC.py)  
### ABC Psuedo Code
```markdown
初始化：
1. 定義食源數量（等於僱傭蜂數量），隨機初始化所有食源的位置。
2. 計算每個食源的適應度（根據優化問題的目標函數）。

迭代過程 4 ~ 7：
重複以下步驟直到達到最大迭代次數或其他終止條件：
3. 僱傭蜂階段：
   a. 對於每個僱傭蜂：
      i. 在其食源周圍選擇一個候選位置。
      ii. 計算候選位置的適應度。
      iii. 如果候選位置的適應度比當前食源更好，則僱傭蜂將這個新位置作為新的食源。

4. 觀察蜂階段：
   a. 對於每個觀察蜂：
      i. 根據僱傭蜂分享的食源質量選擇一個食源，通常概率與食源質量成正比。
      ii. 在選中的食源周圍選擇一個候選位置。
      iii. 計算候選位置的適應度。
      iv. 如果候選位置的適應度比當前食源更好，則觀察蜂將這個新位置作為新的食源。

5. 偵察蜂階段：
   a. 檢查是否有食源超過了一定次數沒有被改善（例如，超過了一定的“試驗限制”）。
   b. 對於每個達到試驗限制的食源，隨機初始化一個新的食源位置。
   c. 計算新食源的適應度。

6. 確定最佳食源：
   a. 更新並記錄找到的最佳食源（如果這一輪產生了更好的解）。

輸出：
7. 輸出最優食源的位置及其適應度值。

```
</details>

<details>
<summary>ACO (Ant Colony Optimization)</summary>

## ACO (Ant Colony Optimization)
透過模擬螞蟻從蟻巢到食物源的最短路徑，螞蟻透過一種稱為`信息素(pheromone)`的化學物質進行間接通訊，透過釋放信息素來記錄走過的路徑，並且影響之後螞蟻如何選擇路徑。    
ACO演算法可以解決旅行銷售員問題（TSP）、車輛路徑問題（VRP）、排程問題和網絡路由問題等。
* 初始化一群螞蟻 (n個)，在node之間每個螞蟻代表一個潛在的解
* 影響螞蟻選擇路徑的有兩個因素
  * 信息素的強度(之前選擇同樣路徑的頻率)
  * 距離
* 為了防止演算法過擬合，使演算法更好的搜索潛在路徑，因此信息素有蒸發機制，會隨著時間遞減

### 轉移規則
$$p_{ij} = \frac{(\tau_{ij}^\alpha) (\eta_{ij}^\beta)}{\sum_{k \in \text{可達節點}} (\tau_{ik}^\alpha) (\eta_{ik}^\beta)}$$
此公式計算  
- 其中 τ_ij 是節點 i 到 j 的信息素濃度
- η_ij 是啟發式信息（如城市間的倒數距離）
- α 和 β 是控制信息素和啟發式信息影響力的參數。  

[ACO程式碼](./ACO.py) 

### ACO Psuedo Code
```md
初始化：
1. 初始化所有路徑上的信息素濃度。
2. 定義參數，例如信息素蒸發率ρ（rho）和信息素強化參數（Q）。

迭代過程：
重複以下步驟直到達到終止條件（如最大迭代次數或解的質量）：
3. 將螞蟻隨機分配到不同的節點（例如，在TSP中的城市）。

4. 每隻螞蟻構建解：
   a. 對於每隻螞蟻，重複以下步驟直到完成解的構建：
      i. 基於轉移規則選擇下一節點。轉移概率 p 計算如轉移規則
   b. 移動到選擇的節點，直到路徑完成。

5. 更新信息素：
   a. 對每條路徑應用蒸發：
      τ_ij = (1 - ρ) * τ_ij
   b. 每隻螞蟻基於其路徑長度 L_k 強化走過的路徑上的信息素：
      Δτ_ij_k = Q / L_k
      τ_ij = τ_ij + Δτ_ij_k
   c. 如果有全局最佳更新，則額外強化全局最佳路徑。

6. 記錄並檢查新的全局最佳解。

輸出：
7. 輸出最佳路徑和相應的路徑長度。

```
</details>

<details>
<summary>FireFly</summary>

## FireFly

</details>

<details>
<summary>GA (Genetic Algorithm)</summary>

## GA (Genetic Algorithm)
</details>