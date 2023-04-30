# Get_stringtie_RNA_matrix
**转录组Hisat2+Stringtie简单定量，处理Stringtie简单定量的结果，以构成矩阵文件**

- **前期处理**
    - 第一步：建立基因组fa的索引
    - ```hisat2-build -f  基因.fasta 索引名字```

    - 第二步：比对构建比对排序后的sam文件
    - ```hisat2 --dta -x genome-index  -1 clean.R1.fastq.gz -2 clean.R2.fastq.gz | samtools view -b -S -|samtools sort -@ 25 > ./${i}.bam```
    - 第三步：开始计算定量：stringtie
    - ```nohup stringtie -p 10 -G ${in_road}/genom.gff3 -e -o ${out1_road}/${i}.gtf -B -A /${out1_road}/${i}.tab ${in1_road}/${i} > ./log/\${i}-log & ```

**本脚本即用在处理${i}.gtf 构建FPKM值得矩阵**

```
python3.0 getFPKM.py -i list -g GENE_FPKM -t TRANSCRIPT_FPKM
```
input list文件应该输入一个制表符分隔的文件，每一行包含样本ID和gtf文件路径，例如：
```
sampleA A.stringtie.gtf
sampleB B.stringtie.gtf
```

需要注意的是
**``输出文件第二行可能是错误的，自己手动删除``**
