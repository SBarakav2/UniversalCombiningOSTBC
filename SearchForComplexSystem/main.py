from FindMaxRate import *


# STBC definitions
stbc1 = Block(block_string="z_{1}   & 0       & z_{2}   & z_{3}  //"
                           "0       & z_{1}   & z_{4}   & z_{5}  //"
                           "-z_{2}* & -z_{4}* & z_{1}*  & 0      //"
                           "-z_{3}* & -z_{5}* & 0       & z_{1}* //"
                           "-z_{4}  & z_{2}   & 0       & z_{6}  //"
                           "0       & -z_{6}* & -z_{3}* & z_{2}* //"
                           "-z_{5}  & z_{3}   & -z_{6}  & 0      //"
                           "z_{6}*  & 0       & -z_{5}* & z_{4}*")

stbc2 = Block(block_string="x_{1}  & x_{2}*  &  x_{3}* //"
                           "x_{2}  & -x_{1}*  & 0     //"
                           "x_{3}  & 0       & -x_{1}*//"
                           "0      & x_{3} &   -x_{2}     ")

stbc3 = Block(block_string="x_{1}  & x_{2}  &  x_{3}     & 0  //"
                           "-x_{2}*  & x_{1}*  & 0       & x_{3}  //"
                           "-x_{3}*  & 0       & x_{1}*  &  -x_{2}  //"
                           "0      & -x_{3}* &   -x_{2}* &  x_{1}    ")

stbc4 = Block(block_string="x_{1}  & x_{2}     &  x_{3}     & 0  //"
                           "-x_{1}  & -x_{2}   &  -x_{3}       & 0  //"
                           "-x_{3}*  & 0       & x_{1}*  &  -x_{2}*  //"
                           "-x_{3}*      & 0   &   -x_{1}* &  x_{2}*    ")  # non orthogonal
print("==================================================================")
stbc = stbc2 # choose an stbc
max_vec, min_times = find_max_rate(stbc, 1, 3)
print('min times: ' + str(min_times))
print('optimal channel vec:')
print(max_vec)
print_full_plot(stbc, max_vec)
