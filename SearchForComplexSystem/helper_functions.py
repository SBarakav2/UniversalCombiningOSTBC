from Tools import *
import pandas as pd

REC_INDEX = 1
TRANS_INDEX = 0


def split_by_receivers(channel_coeff):
    """ The function gets an assignment of channel coefficients, all the coefficients must be double indexed.
    It split the coefficients indices to subgroups according to the receiver number, each subgroup of indices is
    sorted by the transmitter number.
    The result is a dictionary mapping each 'rec number' to list of indices of the corresponding sub-group"""
    if not isinstance(channel_coeff, Block):
        raise TypeError('Channel coefficients must be of type Block.')
    if np.size(channel_coeff, 0) > 1 and np.size(channel_coeff, 1) > 1:
        raise ValueError('Channel coefficients must be a vector.')
    if np.size(channel_coeff, 0) == 1:
        channel_coeff = np.transpose(channel_coeff)
    rec_numbers = [elem[0].symbol.indices_list[REC_INDEX] for elem in channel_coeff]
    trans_numbers = [elem[0].symbol.indices_list[TRANS_INDEX] for elem in channel_coeff]
    original_indices = list(range(len(channel_coeff)))
    d = {'trans num': trans_numbers, 'rec num': rec_numbers, 'index': original_indices}
    df = pd.DataFrame(d)
    return df.sort_values('trans num').groupby('rec num')['index'].apply(list).to_dict()


def get_conjugate_by_receiver(channel_coeff, groups):
    """ The function gets channel coefficients Block and the groups returned from the function above,
    and returns the conjugate sign of each group. If there is a group with inconsistent conjugates the function
    will raise ValueError."""
    if np.size(channel_coeff, 0) == 1:
        channel_coeff = np.transpose(channel_coeff)
    result = {}
    for rec_num in groups:
        first_conj = channel_coeff[groups[rec_num][0], 0].conjugate
        if not all(channel_coeff[x, 0].conjugate == first_conj for x in groups[rec_num]):
            raise ValueError('Each receiver group must contain coefficients with the same conjugate')
        else:
            result[rec_num] = channel_coeff[groups[rec_num][0], 0].conjugate
    return result


def get_desired_groups(desired_mat, groups):
    result = {}
    for rec_num in groups:
        result[rec_num] = np.sum(desired_mat[:, groups[rec_num]], axis=1)
    return result


SUPERSCRIPT_STAR = 0x20F0
SUBSCRIPT_0 = 0x2080


class CombiningElement:

    def __init__(self, rec_num, time):
        self.rec_num = rec_num
        self.time = time
        self.is_conj = False
        self.is_minus = False

    def __repr__(self):
        sign_str = '-' * self.is_minus + '' * (not self.is_minus)
        conj_str = chr(SUPERSCRIPT_STAR) * self.is_conj + '' * (not self.is_conj)
        if self.rec_num == 'none':
            rec_num_str = 'none'
        else:
            rec_num_str = ''
            for char in self.rec_num:  # first index
                rec_num_str += chr(SUBSCRIPT_0 + int(char))
        return sign_str + 'S' + rec_num_str + conj_str + '(' + str(self.time) + ')'


def can_be_expressed(phrase1, phrase2):
    if phrase1 is None or phrase2 is None:
        return False
    if phrase1 == phrase2:
        return {'is_minus': False, 'is_conj': False}
    elif phrase1 == phrase2.minus():
        return {'is_minus': True, 'is_conj': False}
    elif phrase1 == phrase2.conjugate():
        return {'is_minus': False, 'is_conj': True}
    elif phrase1 == phrase2.conjugate().minus():
        return {'is_minus': True, 'is_conj': True}
    else:
        return False


def find_combining_system(stbc, channel_coeff_original):
    # prepare indices_groups, conj_groups and desired_groups
    channel_coeff = deepcopy(channel_coeff_original)
    indices_groups = split_by_receivers(channel_coeff)
    conj_groups = get_conjugate_by_receiver(channel_coeff, indices_groups)
    desired_mat = stbc * channel_coeff
    desired_groups = get_desired_groups(desired_mat, indices_groups)
    # Start Searching
    time = 0
    num_of_tx = desired_groups[next(iter(desired_groups))][0].block1.shape[1]
    num_of_rx = len(desired_groups)
    max_num_of_phrases = max([desired_groups[rec_num].shape[0] for rec_num in desired_groups])
    transmission_matrix = np.array([]).reshape(0, num_of_tx)  # initialize with empty matrix
    combining_matrix = np.full((max_num_of_phrases, num_of_rx), None)
    for rec_ind, rec_num in enumerate(desired_groups):
        for phrase_ind, phrase in enumerate(desired_groups[rec_num]):
            if phrase is None or phrase.is_only_zeros():
                continue
            # find the transmitted symbols
            if conj_groups[rec_num] == '*':
                added_transmission = phrase.conjugate().block1
            else:
                added_transmission = phrase.block1
            # adjust the sign of the transmitted symbols
            rec_coeff = channel_coeff[0, indices_groups[rec_num]]
            # ignore conjugates and sign of rec_coeff
            for coeff in rec_coeff:
                coeff.conjugate, coeff.sign = '', '+'
            transmission_matrix = np.vstack((transmission_matrix, added_transmission))  # concatenate the syms
            # insert the combining element
            comb = CombiningElement(rec_num, time)
            comb.is_minus = False
            comb.is_conj = True if conj_groups[rec_num] == '*' else False
            combining_matrix[phrase_ind, rec_ind] = comb
            # prepare for searching other phrases
            current_phrase = phrase
            desired_groups[rec_num][phrase_ind] = None
            # search for other phrases that can be expressed by the transmitted symbols
            for rx_ind_inner, rec_num_inner in enumerate(desired_groups):
                rec_coeff = channel_coeff[0, indices_groups[rec_num_inner]]
                # ignore conjugates and sign of rec_coeff
                for coeff in rec_coeff:
                    coeff.conjugate, coeff.sign = '', '+'
                rec_phrase = np.sum(added_transmission * rec_coeff, axis=1)
                for phrase_ind_inner, phrase_inner in enumerate(desired_groups[rec_num_inner]):
                    match_result = can_be_expressed(rec_phrase, phrase_inner)
                    if not match_result:
                        continue
                    comb = CombiningElement(rec_num_inner, time)
                    comb.is_minus, comb.is_conj = match_result['is_minus'], match_result['is_conj']
                    combining_matrix[phrase_ind_inner, rx_ind_inner] = comb
                    desired_groups[rec_num_inner][phrase_ind_inner] = None
            time += 1  # increment time
    return transmission_matrix, combining_matrix


def print_full_plot(stbc, channel_coeff):
    print("===========================================================================================")
    print("===========================================================================================")
    print("========================================= Inputs ==========================================")
    print("STBC:")
    print(stbc)
    print('---------------------------------------------')
    print("Channel coefficients:")
    print(channel_coeff)
    print("================================== Intermidiate Results ===================================")
    print("Indices:")
    group_indices = split_by_receivers(channel_coeff)
    print(group_indices)
    print('---------------------------------------------')
    print("Conjugates groups:")
    print(get_conjugate_by_receiver(channel_coeff, group_indices))
    desired_mat = deepcopy(stbc) * deepcopy(channel_coeff)
    print('---------------------------------------------')
    print("Desired Phrases:")
    print(np.sum(desired_mat, axis=1))
    desired_groups = get_desired_groups(desired_mat, group_indices)
    for rec_num in desired_groups:
        print("Desired phrases for receiver " + rec_num)
        print(desired_groups[rec_num])
    print('---------------------------------------------')
    print("========================================= Output =========================================")
    transmission_matrix, combining_matrix = find_combining_system(stbc, channel_coeff)
    print("Transmission Matrix:")
    print(transmission_matrix)
    print("Combining Scheme:")
    print(combining_matrix)
    print("========================================= Summary =========================================")
    print("Minimum channel uses: " + str(transmission_matrix.shape[0]))


