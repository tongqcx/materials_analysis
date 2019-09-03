# ATCNN
ATCNN is a ML model for properties prediction of materials based on CNN and atom table represetation which only use the component information.
For more information about ATCNN, please read [npj Computational Materials 5, 84 (2019)](https://www.nature.com/articles/s41524-019-0223-y)
## Usage:
### Training: 
     python main.py -t  --datapath=the path of your dataset  

### Test:  
     python main.py -p --datapath=the path of your dataset  

### For more information type   
     python main.py -h  
### The example of dataset
     Al1K1O6Si2      -3.144727
     Al2H4O9Si2      -2.499380 
     Al1H1O2         -2.589914 
     Al1H1O2         -2.566077 
     Al2Fe1O4        -2.932896 
     Ac1              0.000000 
     Ag1              0.000000 
     The first colume is formula, and the second colume is properties you want to predict, such as formation energy per formula or superconducting transition temperatures(Tc)
