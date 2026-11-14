
def levenshtein_distance(word1, word2):

    m = len(word1)
    n = len(word2)

    # Create a matrix of size (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize first column
    for i in range(m + 1):
        dp[i][0] = i

    # Initialize first row
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, m + 1):

        for j in range(1, n + 1):

            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1

            deletion = dp[i - 1][j] + 1

            insertion = dp[i][j - 1] + 1

            substitution = dp[i - 1][j - 1] + cost

            dp[i][j] = min(
                deletion,
                insertion,
                substitution
            )

    return dp[m][n]
