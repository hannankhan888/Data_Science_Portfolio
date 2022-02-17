library(tidyverse)

# we load the csv data from 2021:
df <- read_csv("D:\\Datasets\\Divvy_Trips_Data\\Divvy_Trips_2021\\2021_all_data.csv")

# we peek at the data:
head(df)

# we look at the structure of the data:
str(df)

# lets look at just the column names:
colnames(df)

# one of the columns "..1" is incorrectly labeled, let's rename it:
df <- rename(df, index = "...1")

# check to see the column has been renamed:
colnames(df)

# lets make sure all columns have clean names:
library(janitor)
clean_names(df)

# look at null values for our data frame by column:
colSums(is.na.data.frame(df))

# clean the column with the largest null values first:
# dropping end_station_name:
df <- drop_na(df, end_station_name)

# checking to see if na values are dropped:
colSums(is.na.data.frame(df))

# there are more na values in start_station_name, let's drop them:
df <- drop_na(df, start_station_name)

# check again to see if na values are dropped:
colSums(is.na.data.frame(df))

# Great! Now we can continue cleaning the data:
# let's see if there are any duplicates. Since ride_id acts as a primary key, we
# can use it to check for duplicate data:
get_dupes(df, ride_id)

# lets look at the structure of the data again:
str(df)

# since the start/end times do not have a datetime format, we will include it:
df[["started_at"]] <- as.POSIXct(df[["started_at"]],
                                 format = "%Y-%m-%d %H:%M:%S")
df[["ended_at"]] <- as.POSIXct(df[["ended_at"]],
                               format = "%Y-%m-%d %H:%M:%S")

# lets check to see if the formatting has worked:
sapply(df, class)

# cool, now we are done with data cleaning, let's add another column,
# and call it ride_length:
df <- df %>%
  mutate(ride_length = as.numeric(difftime(ended_at,started_at,units="secs"),
                                  units="secs"))

# lets take a peek at the data:
sapply(df, class)
str(df)

# we can also create a 'day of week' value:
df <- df %>%
  mutate(weekday = weekdays(df$started_at))

# lets take another peek at the data:
sapply(df, class)
str(df)

# we can find the starting time of day for each ride (morning, afternoon, evening):
# {
#   morning:    00:00:00-11:59:59
#   afternoon:  12:00:00-17:59:59
#   evening:    18:00:00-23:59:59
# }
# src: https://stackoverflow.com/questions/62419598/r-convert-time-to-time-of-day
library(lubridate)
get_time_of_day <- function(start_time) {
  hour_time <- hour(start_time)
  case_when(hour_time >= 0 & hour_time <= 11 ~ 'morning',
            hour_time >= 12 & hour_time <= 17 ~ 'afternoon',
            hour_time >= 18 & hour_time <= 23 ~ 'evening')
}
df <- df %>%
  mutate(time_of_day = get_time_of_day(started_at))

# lets take a peek at the data:
str(df)

# lets check to see if any NA values were produced from our function:
colSums(is.na.data.frame(df))



