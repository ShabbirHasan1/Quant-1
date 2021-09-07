# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 18:55:11 2021

@author: User
"""

# Trying VADER

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
analyser.polarity_scores('This is a good course')
analyser.polarity_scores('This is an awesome course')
analyser.polarity_scores('This is such a great course omg')
analyser.polarity_scores('The instructor is so cool!')
analyser.polarity_scores('I love you!')
analyser.polarity_scores('Fuck you!')
analyser.polarity_scores("I don't love you anymore" )
analyser.polarity_scores("Yay This stock is going crazy")
analyser.polarity_scores("Wow This is crazy")
