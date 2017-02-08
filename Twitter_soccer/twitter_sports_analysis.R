'
Author: Rory Pulvino
Date: Jan. 20, 2017
Title: Twitter Sports Sentiment Analysis
'
################################################################
############             Packages                 ##############
################################################################

pkgs <- c("purrr", "data.table", "dplyr", "tidyr", "readr", "lubridate", "stringr",
          "ggplot2", "igraph", "tidytext", "FactoMineR", "openNLP", "fpc", "wordcloud")
allLoaded <- sapply(pkgs, require, character.only = TRUE)

################################################################
############             Data                     ##############
################################################################

df <- read.csv("~/Dropbox/Python/jupyter-blog/content/Twitter_soccer/Tweets_sports.csv", header = TRUE)

################################################################
############             Tidying data             ##############
################################################################

'Website guidance: http://varianceexplained.org/r/trump-tweets/
'
reg <- "([^A-Za-z\\d#@']|'(?![A-Za-z\\d#@]))"

# Creating a tokenized data frame where each row is a word from a tweet
tweet_words <- df %>% 
  filter(!str_detect(Text, '^"') & !str_detect(Text, '^RT')) %>% # Removes tweets that are quotes or retweets as these are not the users' own words
  mutate(Text = str_replace_all(Text, "https://t.co/[A-Za-z\\d]+|&amp;", "")) %>% # Removing links
  mutate(Text = str_replace_all(Text, "http://t.co/[A-Za-z\\d]+|&amp;", "")) %>% # Removing links
  unnest_tokens(word, Text, token = "regex", pattern = reg, to_lower = TRUE) %>%
  filter(!word %in% stop_words$word,
         str_detect(word, "[a-z]")) # Removing 'stop words' 

################################################################
############             Exploring data           ##############
################################################################
women_top_words <- tweet_words %>% # Dataset of top words from female tweeters
  filter(Sex == 'F') %>%
  count(word, sort = TRUE)

men_top_words <- tweet_words %>% # Dataset of top words from male tweeters
  filter(Sex == 'M') %>%
  count(word, sort = TRUE)

# Graphing top words by gender
ggplot(data = subset(men_top_words, n > 1000))+
  geom_bar(aes(factor(word), y = n), stat = 'identity', fill = 'darkorange', colour = 'dodgerblue')+
  coord_flip(ylim = c(0,3200))+
  labs(title = "Top Words used by Male Tweeters",
       y = "Number of Instances", x = "Word")

ggplot(data = subset(women_top_words, n > 730))+
  geom_bar(aes(factor(word), y = n), stat = 'identity', fill = 'darkorange', colour = 'dodgerblue')+
  coord_flip(ylim = c(0,2400))+
  labs(title = "Top Words used by Female Tweeters",
       y = "Number of Instances", x = "Word")


################################################################
############             Analyzing data           ##############
################################################################



