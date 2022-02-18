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

















# Now we are at the analysis/visualization portion of our report.
ordered_weekdays <- c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                      "Friday", "Saturday")
library(scales)
# First, we can compute basic statistics about each of our member types.
# src: https://www.tutorialspoint.com/r/r_mean_median_mode.htm
mode_calc <- function (v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}
df %>%
  group_by(member_casual) %>%
  summarize(count = n(),
            mean_ride_len_s = mean(ride_length),
            mean_ride_len_m = mean(ride_length)/60,
            max_ride_len_s = max(ride_length),
            max_ride_len_m = max(ride_length)/60,
            most_common_wkday = mode_calc(weekday)) %>%
  datatable() %>%
  formatRound(c("mean_ride_len_s", "mean_ride_len_m", "max_ride_len_m"), 1)

# calculate most common days of week by member type:
# (number of rides per day by member type)
df %>%
  group_by(member_casual, weekday) %>%
  summarize(observations = n()) %>%
  pivot_wider(names_from = weekday, values_from = observations) %>%
  select(ordered_weekdays) %>%
  datatable()

ggplot(df, mapping=aes(x=weekday, fill=rideable_type)) +
  geom_bar() +
  facet_wrap(~member_casual) +
  labs(x = "Weekday",
       y = "Count",
       title = "Number Of Rides Per Day By Member Type") +
  scale_x_discrete(limits = ordered_weekdays) +
  scale_y_continuous(labels = label_number_si()) +
  scale_fill_brewer(name = "Rideable Type", labels = c("Classic Bike", "Docked Bike", "Electric Bike"),
                    palette = "Blues") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45))

# average ride length by day of week:
df %>%
  group_by(member_casual, weekday) %>%
  summarize(avg_ride_len = mean(ride_length)) %>%
  pivot_wider(names_from = weekday, values_from = avg_ride_len) %>%
  select(ordered_weekdays) %>%
  datatable() %>%
  formatRound(ordered_weekdays, 1)

ggplot(df,mapping = aes(x = weekday, y = ride_length)) +
  geom_bar(stat = "summary", fun = "mean", fill = "#3288bd") +
  facet_wrap(~member_casual) +
  labs(x = "Weekday",
       y = "Average Ride Length",
       title = "Average Ride Length By Weekday Based On Member Type") +
  scale_x_discrete(limits = ordered_weekdays) +
  scale_y_continuous(labels = label_number_si(accuracy = 0.1)) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45),
        legend.position = "none")

# what is the most popular time of day for different members?
df %>%
  group_by(member_casual, time_of_day) %>%
  summarize(observations = n()) %>%
  pivot_wider(names_from = time_of_day, values_from = observations) %>%
  select(c("morning", "afternoon", "evening")) %>%
  datatable()

ggplot(df, mapping = aes(x = time_of_day)) +
  geom_bar(fill = "#3288bd") +
  facet_wrap(~member_casual) +
  labs(x = "Time Of Day",
       y = "Count",
       title = "Time Of Day Based On Member Type") +
  scale_x_discrete(limits = c("morning", "afternoon", "evening")) +
  scale_y_continuous(labels = label_number_si()) +
  theme_minimal()

install.packages('DT')
library(DT)










