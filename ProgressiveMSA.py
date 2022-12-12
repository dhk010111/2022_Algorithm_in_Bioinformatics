import time

# sequences 입력 받는 함수
def get_sequences():
    sequences = []  # sequences는 1차원 배열 변수 이름.

    print('[sequence 수 입력]')
    n = int(input())  # sequence 수 입력. 정수형.

    print('[sequence 입력]')
    for i in range(n):  # sequences 수 만큼,
        sequences.append(input())  # sequence를 입력 받아, sequences에 저장.

    return sequences  # 저장된 sequences를 반환.

# 한 쌍씩 sequence 정렬, 기준이 되는 sequence 결정하는 함수 호출.
def get_center(sequences):
    score_matrix = {}  # null로 초기값 설정.
    # 0 부터 sequence 개수 만큼 반복.
    for i in range(len(sequences)):
        score_matrix[i] = {}  # 행 생성, null로 초기값 설정.

    # 한 쌍씩 sequence 묶어서 정렬한 값 배열에 저장.
    for i in range(len(sequences)):  # 0~n-1 까지 반복.
        for j in range(len(sequences)):  # 0~n-1 까지 반복.
            if i != j:  # i와 j가 같지 않다면,
                # global sequence alignment로 쌍씩 정렬하는 함수 호출.
                # 정렬된 시퀀스x, 시퀀스y, 테이블 마지막 계산 결과값(숫자) 배열에 저장.
                score_matrix[i][j] = global_alignment(sequences[i], sequences[j], 1, -1, -1)
                ##print(score_matrix[i][j])

    center = 0  # 정수형 변수 선언
    center_score = float('-inf')  # 음의 무한대

    # 중심 시퀀스가 배열에 저장된 위치 번호 찾기.
    for i in score_matrix:     # score_matrix 숫자
        sum = 0  # scores가 바뀔 때마다 sum은 0으로 초기화
        # 고정 scores, i 의 정렬 마지막 값을 모두 합하여 sum에 저장
        for j in score_matrix[i]:
            ##print('시퀀스 번호', i,j)
            ##print(score_matrix[scores][i][2])
            sum += score_matrix[i][j][2]  # 마지막 값인, 테이블 마지막 계산 결과값을 가져와 sum에 더해준다.

        # 기준이 되는 시퀀스가 배열에 저장된 위치 번호 찾기.
        if sum > center_score:      # sum 값이 초기값 음수 보다 크면,
            center_score = sum      # cente_score은 sum 값을 같게 된다.
            center = i
            ##print('중심 시퀀스 번호', center)

    alignments_needed = {}  # 재정렬된 시퀀스 저장될 배열 선언.
    # 중심 시퀀스 기준으로 나머지 시퀀스와 재정렬
    for i in range(len(sequences)):  # 0 ~ n-1 까지 반복.
        if i != center:     # sum이 center_score 보다 클 때의 score의 값 = center가 i랑 같지 않다면,
            ##print('재정렬될 한 쌍 정보', sequences[i],sequences[center])
            # 중심이 되는 기준 시퀀스와 나머지 시퀀스가 한쌍을 이뤄, 재정렬.
            s1, s2, sc = global_alignment(sequences[i], sequences[center], 1, -1, -1)
            alignments_needed[i] = (s2, s1, sc)  # s2,와 s1의 위치를 바꾸어 배열에 저장


    #print('재정렬된 시퀀스', alignments_needed)

    return center, alignments_needed    # 기준이되는 시퀀스 배열 위치 값, 재정렬된 시퀀스가 들어간 배열 반환


# global sequence alignment 함수
def global_alignment(x, y, match, mismatch, gap):

    A = []  # 계산될 테이블 생성

    # sequence 테이블 생성 및 초기화
    for i in range(len(y) + 1):  # 전체 테이블 값 0으로 초기화
        A.append([0] * (len(x) + 1))
    for i in range(len(y) + 1): # 첫 열의 행 값 계산
        A[i][0] = gap * i
    for i in range(len(x) + 1): # 첫 행의 열 값 계산
        A[0][i] = gap * i

    # A[1][1] 부터 값 계산
    for i in range(1, len(y) + 1):  # 1부터 sequence y 문자열 길이 +1 까지 반복
        for j in range(1, len(x) + 1):  # 1부터 sequence x 문자열 길이 +1 까지 반복
            # 최대값 A[i][j]에 저장
            A[i][j] = max(
                A[i][j - 1] + gap,
                A[i - 1][j] + gap,
                # 같고 sequence y의 i-1번째가 '-' 이면 match,
                # 다르고 sequence y의 j-1번째가 '-' 이 아니면 mismatch,
                # sequence x의 i-1번째가 '-' 또는 sequence y의 j-1번째가 '-'이면 gap을 더한다.
                A[i - 1][j - 1] + (match if (y[i - 1] == x[j - 1] and y[i - 1] != '-') else 0) + (
                    mismatch if (y[i - 1] != x[j - 1] and y[i - 1] != '-' and x[j - 1] != '-') else 0) + (
                    gap if (y[i - 1] == '-' or x[j - 1] == '-') else 0)

            )
    """
    print('[풀이과정]')
    for i in A:
        for j in i:
            print(j, end= ' ')
        print()
    print()
    """

    i = len(x)  # x의 문자열 길이
    j = len(y)  # y의 문자열 길이

    Xa = ""
    Ya = ""

    while i > 0 or j > 0:
        current_score = A[j][i]
        if i > 0 and j > 0 and (
                ((x[i - 1] == y[j - 1] and y[j - 1] != '-') and current_score == A[j - 1][i - 1] + match) or
                ((y[j - 1] != x[i - 1] and y[j - 1] != '-' and x[i - 1] != '-') and current_score == A[j - 1][
                    i - 1] + mismatch) or
                ((y[j - 1] == '-' or x[i - 1] == '-') and current_score == A[j - 1][i - 1] + gap)
        ):
            Xa = x[i - 1] + Xa
            Ya = y[j - 1] + Ya
            i -= 1
            j -= 1
        # sequence y 에 gap '-' 추가하는 경우,
        elif i > 0 and (current_score == A[j][i - 1] + gap):
            Xa = x[i - 1] + Xa
            Ya = "-" + Ya
            i -= 1
        # sequence x에 gap '-' 추가하는 경우,
        else:
            Xa = "-" + Xa
            Ya = y[j - 1] + Ya
            j -= 1
    """
    print('[score 점수]')
    print(current_score)
    """
    ##print(Xa)
    ##print(Ya)
    ##print(A[len(y)][len(x)])

    # 2개의 sequence 정렬 값, A 배열 마지막 값 = score 계산 마지막 값 반환
    return (Xa, Ya, A[len(y)][len(x)])

# 재정렬된 한쌍 씩의 시퀀스를 서로 비교하여, gap추가하는 함수
def msa(alignments):
    aligned_center = alignments[list(alignments.keys())[0]][0]  # 배열 첫번째 sequence 값 지정.
    ##print(aligned_center)

    aligneds = [] # 시퀀스 길이에 맞춰 gap이 추가된 sequences가 저장될 배열 생성
    aligneds.append(alignments[list(alignments.keys())[0]][1])  # 배열 두번째 sequence 값 배열에 저장.
    ##print(aligneds)

    for seq in list(alignments.keys())[1:]:     # 2번째 부터~끝 list(alignments.keys())[1:] = seq
        cent = alignments[seq][0]   # seq 행의 첫번째 값 지정.
        ##print("cent",cent)
        newsequence = alignments[seq][1]    # seq 행의 두번째 값 지정.
        ##print('newsequence',newsequence)

        # 빈 공간에 gap 추가하는 함수('-')
        aligned_center, aligneds = align_gaps(aligned_center, cent, aligneds, newsequence)
        ##print(aligned_center, aligneds)

    return aligneds, aligned_center     #gap 추가된 배열값, 중심 sequence값 반환

# 빈 공간에 gap 추가하는 함수('-')
def align_gaps(seq1, seq2, aligneds, new):
    i = 0   # i 초기값 설정
    # seq1과 seq2 중에 문자열 길이가 더 긴 것을 기준으로, i보다 클 경우.
    while i < max(len(seq1), len(seq2)):     # seq2에서 정렬된 seq = seq1
        try:
            if i > len(seq1)-1:         # seq1 문자열 길이 -1이 i보다 작으면,
                seq1 = seq1[:i] + "-" + seq1[i:]    # seq1의 i번째 문자 뒤에 -를 추가 후 i번째 이후 문자열로 다시 저장
                naligneds = []
                for seq in aligneds:
                    naligneds.append(seq[:i] + "-" + seq[i:])   # naligneds에 seq의 i번째 문자 뒤에 - 추가 후 i번째 이후 문자열 추가
                aligneds = naligneds    # 추가된 naligneds  값을 aligneds에 저장
            elif i> len(seq2)-1:    # seq2 문자열 길이 -1이 i 보다 작으면,
                seq2 = seq2[:i] + "-" + seq2[i:]    # seq2의 i번째 문자 뒤에 -를 추가 후 i번째 이후 문자열로 다시 저장
                new = new[:i] + "-" + new[i:]       # new의 번째 문자 뒤에 -를 추가 후 i번째 이후 문자열로 다시 저장
            # seq1의 i번째 자리에 -가 있고 i가 seq2 문자열 길이보다 같거나 긴 경우나, seq2의 i가 -이 아닌 경우에,
            elif (seq1[i] == "-" and i>= len(seq2)) or (seq1[i] == "-" and seq2[i] != "-"):
                seq2 = seq2[:i]+"-"+seq2[i:]    # seq2의 i번째 문자 뒤에 -를 추가 후 i번째 이후 문자열로 다시 저장
                new = new[:i]+"-"+new[i:]       # new의 번째 문자 뒤에 -를 추가 후 i번째 이후 문자열로 다시 저장
            # seq2의 i번째 자리에 -가 있고 i가 seq1 문자열 길이보다 같거나 긴 경우나, seq2의 i가 -이 아닌 경우에,
            elif (seq2[i] == "-" and i>= len(seq1)) or (seq2[i] == "-" and seq1[i] != "-"):
                #print("me")
                seq1 = seq1[:i] + "-" + seq1[i:]    # seq1의 i번째 문자 뒤에 -를 추가 후 i번째 이후 문자열로 다시 저장
                naligneds = []
                for seq in aligneds:
                    naligneds.append(seq[:i] + "-" + seq[i:])   #  naligneds에 seq의 i번째 문자 뒤에 - 추가 후 i번째 이후 문자열 추가
                aligneds = naligneds    # 추가된 naligneds  값을 aligneds에 저장

        except:
            print("error")
        i += 1    # i = i+1
    aligneds.append(new)    # new의 값 aligneds에 추가

    ##print('seq1 = ',seq1)
    ##print('aligneds = ',aligneds)
    return seq1, aligneds   # seq1, aligneds 반환

# 정렬한 sequences을 result 배열에 순서 대로 저장하는 함수
def get_results(aligneds, center_seq, center):
    i = 0
    j = 0
    results = []    # 정렬한 sequences을 저장할 배열 변수 선언.
    while i < len(sequences):
        if i == center:
            results.append(center_seq)  # center sequence 배열에 추가.
            i += 1
        else:
            results.append(aligneds[j])     # 순차적으로 배열에 추가.
            i += 1
            j += 1
    return results      # 결과값 반환

# # 최종 정렬된 값으로 점수 매기는 함수
def calculate_scores(alignments):
    score = 0   # 점수가 저장될 변수 선언 및 초기값 0으로 설정.

    for i in range(len(alignments[0])):     # 0~ 첫번째 sequence의 길이-1까지 반복.
        for j in range(len(alignments)-1):  # 0~ 첫번째 sequence의 길이-1-1까지 반복.
            for k in range(j+1,len(alignments)):    # j+1 ~ n-1까지
                # 같은 위치의 값이 같다면,
                if alignments[j][i] == alignments[k][i]:    # 몇 번째 sequence의 몇 번 째에 위치한 문자
                    if alignments[j][i]!="-":   #  '-'이 아닌 경우 = acgt 중에서 문자가 같다는 의미
                        score +=1   # match 이므로, 점수 1점 더해준다.
                elif alignments[k][i]=="-" or alignments[j][i]=="-":    # 같은 위치에 둘 중 하나가 '-'이면,
                    score-=1    # gap 이므로, 점수에 1점을 빼준다.
                else:   # 그 외의 경우(dismatch), 점수에 1점을 뺴준다.
                    score-=1
    return score    # 계산된 점수값 반환


# main 함수
if __name__ == '__main__':
    sequences = get_sequences()  # sequence 수와 sequence 정보 입력 받는 함수 호출.
    start = time.time()
    center, alignments = get_center(sequences)  # 한 쌍씩 sequence 정렬, 기준이 되는 sequence 결정하는 함수 호출.
    aligneds, center_sequence = msa(alignments) # 재정렬된 한쌍 씩의 시퀀스를 서로 비교하여, gap추가하는 함수 호출.
    results = get_results(aligneds, center_sequence, center)  # 최종 정렬된 값을 입력 시퀀스 순서에 맞게 저장하는 함수 호출.
    score=calculate_scores(results)     # 최종 정렬된 값으로 점수 매기는 함수 호출
    align_time = time.time() - start
    print('정렬 실행 시간 :', align_time)
    print('점수 : ',score)    # 점수 출력
    # 최종 정렬 값 출력
    for i in results:
        print(i)


"""
3
AGCCTAGGACTAG
ACCTGGAGAT
TACGCCATTA

6
CTGATCATCGACCGGGATGA
CTGCTCATCGAGAGGGATCA
CTGCTCATCGAGCCGCATGA
CTGCGCATCGAGCGGGTTGA
CTGCTCATCCAGCGGGTTGA
CTGCTCATAGAGAGGGATGA

"""