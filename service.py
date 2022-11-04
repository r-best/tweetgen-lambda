import numpy as np
import random

def preprocess(tweets):
	return tweets

def buildModel(tweets, N):
	P1 = list() 							# index -> number of occurences
	n1_index_mapping = dict() 				# string (n1gram) -> index in P1
	token_index_mapping = dict() 			# string (token) -> index in tokens

	P = np.zeros((1,1), dtype=np.float32) 	# (n1gram index, token index) -> number of occurences of the ngram made from n1gram+token

	num_unique_tokens = 0
	for tweet in tweets:
		words = tweet.split()
		if len(words) < N:
			continue

		words = ["<start>"]*(N-1) + words + ["<end>"]*(N-1)

		for i in range(N-1, len(words)):
			# Construct (N-1)-gram from each word and the N-2 tokens behind it & increment its frequency
			n1gram = " ".join(words[i-N+1:i])
			if n1gram not in n1_index_mapping:
				# print(n1gram)
				n1_index_mapping[n1gram] = len(P1)
				P1.append(0)
				if len(P1) > 1:
					P = np.vstack((P, np.zeros((1,P.shape[1]))))
			P1[n1_index_mapping[n1gram]] += 1

			# Add this token to the tokens array if not already present
			token = words[i]
			if token not in token_index_mapping:
				token_index_mapping[token] = num_unique_tokens
				num_unique_tokens += 1
				if num_unique_tokens > 1:
					P = np.hstack((P, np.zeros((P.shape[0],1))))

			# Construct N-gram by adding next token to (N-1)-gram & increment its frequency
			P[n1_index_mapping[n1gram],token_index_mapping[token]] += 1
			# print(n1gram + " | " + token)

	P /= np.atleast_2d(P1).T
	return P, n1_index_mapping, token_index_mapping

def generateTweet(N, P, n1_index_lookup, token_index_lookup):
	tweet = ["<start>"]*(N-1)
	while tweet[-1] != "<end>":
		r = random.random()
		counter = 0.0

		lastN1Words = " ".join(tweet[-N+1:])

		for token in token_index_lookup:
			if lastN1Words not in n1_index_lookup or \
				P[n1_index_lookup[lastN1Words],token_index_lookup[token]] == 0:
				continue

			counter += P[n1_index_lookup[lastN1Words],token_index_lookup[token]]
			if counter > r:
				tweet += [token]
				break
	tweet = " ".join(tweet)
	return postprocess(tweet)

def postprocess(tweet):
	return tweet
