# AskSummoner

Thought that it would be fun to experiment with the API from the company that allows me to play a great game on my free time
(AKA League of Legends). In exploring this API, I found that there are so many cool and interesting things that I can make out
of it. This project is meant to explore other summoners (or players) in your game. The end goal of this project is to incorporate all the possible API methods to eventually create a Discord bot that allows players to ask about the players that they are up against - hence the name AskSummoner. 

**I haven't worked on this project in a very long time, but have continued to do so now because it felt like a lot of work could have been done on it.**
My main goals of this project are to facilitate a better understanding of SQL for myself. Though I have taught myself the basics of the language and its uses in data science, I hope to put it into practice by compressing the runtime of my algorithm when fetching the latest champion stats for a summoner.

# Inspiration

Most of the inspiration that I got from creating this application, was in part due to the fact that I used third party resources when playing the game (no, it wasn't for cheating, but an app known as Blitz). Blitz contained features in 'champion select' that would describe the players on your team and players on the other team. I knew that these minimal descriptons were true and relied on data to support it. Though, AskSummoner aspires to do the same thing that Blitz and other programs do, I was very interested in trying it as well as well as learning more about Python in the process.

## Frameworks Used

The entire application runs on Python and now on MySQL, as well

Most of the data found is very clunky and makes the overall runtime very tedious for the user. I noticed that most of the data that I was collecting (even though minimal) was taking an average runtime of 19 to 21 seconds. For a Discord bot, that's quite upsetting. To drive more efficiency to minimize the runtime, I have chosen to store these values in a database - that way I wouldn't have to iterate over stats that I already have in my database.

## Functionality of the Application

- [x] Allowed to search summoners
- [x] Find all their ranks in solo/duo queue and flex queue
- [x] Find their most played champions based on mastery
- [x] Display most recent match history
- [x] Implement as Discord bot
- [x] Differentiate the average of all KDA on a champion to most recent games of that champion KDA
- [x] Determine most played champ of recent history

## Currently Working On

- [ ] Making the run time of the differentiation of average kda faster than it currently is
- [ ] Integrate MySQL into getStats method

## Problems that I ran into

In working with the API and gathering necessary information for the bot, I realized that the Match API that Riot supplies is very faulty with their matchlist parameters. What this means is that when you enter a specific season for the matchlists, much more matches are brought back in the response. As a result, I realized that this information can be gathered from an existing source (AKA op.gg). Though they managed to gather all the proper information from Riot's API to show the correct matchlists, it makes more sense to rely on the information that they had already gathered. With op.gg's information on a summoner's champion KDA, I still will have to use Riot's Match API in determining whether the summoner has improved their plays with their champion.

## Things to add in the future

- [ ] Calculate average rank in recent matches
- [ ] Is summoner good/bad in CS'ing (killing minions)
- [ ] Is summoner a bad warder

