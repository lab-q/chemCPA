# Prediction Model

暂且将本模型称作【Prediction Model】：Prediction Model作用是使用作者训练好的模型，进行细胞基因表达的预测。需要下载相关文件：

1. 模型权重：下载链接：[Final models weight checkpoints](https://f003.backblazeb2.com/file/chemCPA-models/chemCPA_models.zip)，模型文件：“27b401db1845eea26c102fb614df9c33.pt”
2. 数据集（供测试用）：下载链接：[Shared gene set](https://f003.backblazeb2.com/file/chemCPA-datasets/sciplex_complete_middle_subset_lincs_genes.h5ad)，可从本数据集中读取某个细胞的cell expression来测试Predict Model

模型文件下载之后，即可使用相关文件进行predict：

- `src`: 用来存放模型权重文件，数据集等
- `geneInfer.py`: 引入`chemCPA.model`中的`ComPert`，封装成类`geneInfer`。
  - 类中加载模型权重文件，并定义predict方法用来进行gene expression的预测。
  - 实例化对象ae，predict时，需要接收的4个输入为：[gene expression, drug name, cell type dose]
- `main.py`: 调用`geneInfer.py`脚本中的对象ae，进行gene expression预测
  - 现脚本中，为方便展示，所以加载了作者处理好的数据集中的gene expression和perturbation，
  - 具体应用中，可根据实际情况加载gene expression和perturbation。



