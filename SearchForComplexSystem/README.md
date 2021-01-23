# UniversalCombiningOSTBC

Description
-------------------------------------------------------------

The script searches over all possible transmission-combining schemes for General N_t x N_r antennas system.
The main.py script enables to define an STBC and run the search over all possible schemes that use symmetric-conjugate space-time encoding.

Steps
-------------------------------------------------------------
1. Define an STBC, using the following format:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
stbc3 = Block(block_string="x_{1}  & x_{2}  &  x_{3}     & 0  //"
                           "-x_{2}*  & x_{1}*  & 0       & x_{3}  //"
                           "-x_{3}*  & 0       & x_{1}*  &  -x_{2}  //"
                           "0      & -x_{3}* &   -x_{2}* &  x_{1}    ")
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2. Call to 'find_max_rate(stbc, N_t, N_r)' to find the the 'channel conjugate-symmetric reordering transformation' vector ('max_vec') that leads to the maximum rate transmission-combining scheme.
3. Call to 'print_full_plot(stbc, max_vec) to print the full transmission-combining scheme (including imidiate results that explain how it was constructed).

Running Progress
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
==================================================================
Total iterations: 24
iter:0,current times:6, min times: 6
iter:1,current times:6, min times: 6
iter:2,current times:6, min times: 6
iter:3,current times:6, min times: 6
iter:4,current times:6, min times: 6
iter:5,current times:6, min times: 6
iter:6,current times:5, min times: 5
iter:7,current times:5, min times: 5
iter:8,current times:5, min times: 5
iter:9,current times:5, min times: 5
iter:10,current times:5, min times: 5
iter:11,current times:5, min times: 5
iter:12,current times:5, min times: 5
iter:13,current times:5, min times: 5
iter:14,current times:5, min times: 5
iter:15,current times:5, min times: 5
iter:16,current times:5, min times: 5
iter:17,current times:5, min times: 5
iter:18,current times:5, min times: 5
iter:19,current times:5, min times: 5
iter:20,current times:5, min times: 5
iter:21,current times:5, min times: 5
iter:22,current times:5, min times: 5
iter:23,current times:5, min times: 5
min times: 5
optimal channel vec:
        0       1       2
0   h₀₋₀    h₀₋₁    h₀₋₂⃰



Output Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
===========================================================================================
===========================================================================================
========================================= Inputs ==========================================
STBC:
      0     1     2
0   x₁    x₂⃰   x₃⃰
1   x₂   -x₁⃰   0  
2   x₃    0    -x₁⃰
3   0     x₃   -x₂ 
---------------------------------------------
Channel coefficients:
        0       1       2
0   h₀₋₀    h₀₋₁    h₀₋₂⃰
================================== Intermidiate Results ===================================
Indices:
{'0': [0], '1': [1], '2': [2]}
---------------------------------------------
Conjugates groups:
{'0': '', '1': '', '2': '*'}
---------------------------------------------
Desired Phrases:
                                                           0
0  +   x₁  •  h₀₋₀    +   x₂⃰ •  h₀₋₁    +   x₃⃰ •  h₀₋₂⃰   
1  +   x₂  •  h₀₋₀    -   x₁⃰ •  h₀₋₁    +   0   •  h₀₋₂⃰   
2  +   x₃  •  h₀₋₀    +   0   •  h₀₋₁    -   x₁⃰ •  h₀₋₂⃰   
3  +   0   •  h₀₋₀    +   x₃  •  h₀₋₁    -   x₂  •  h₀₋₂⃰   
Desired phrases for receiver 0
                     0
0  +   x₁  •  h₀₋₀    
1  +   x₂  •  h₀₋₀    
2  +   x₃  •  h₀₋₀    
3  +   0   •  h₀₋₀    
Desired phrases for receiver 1
                     0
0  +   x₂⃰ •  h₀₋₁    
1  -   x₁⃰ •  h₀₋₁    
2  +   0   •  h₀₋₁    
3  +   x₃  •  h₀₋₁    
Desired phrases for receiver 2
                     0
0  +   x₃⃰ •  h₀₋₂⃰   
1  +   0   •  h₀₋₂⃰   
2  -   x₁⃰ •  h₀₋₂⃰   
3  -   x₂  •  h₀₋₂⃰   
---------------------------------------------
========================================= Output =========================================
Transmission Matrix:
[[ x₁ ]
 [ x₂ ]
 [ x₃ ]
 [ x₂⃰]
 [-x₁⃰]]
Combining Scheme:
[[S₀(0) S₁(3) S₂⃰(2)]
 [S₀(1) S₁(4) None]
 [S₀(2) None -S₂⃰(0)]
 [None S₁(2) -S₂⃰(3)]]
========================================= Summary =========================================
Minimum channel uses: 5

Process finished with exit code 0
