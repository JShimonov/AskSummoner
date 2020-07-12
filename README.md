# AskSummoner

Thought that it would be fun to experiment with the API from the company that allows me to play a great game on my free time
(AKA League of Legends). In exploring this API, I found that there are so many cool and interesting things that I can make out
of it. This project is meant to explore other summoners (or players) in your game. The end goal of this project is to incorporate all the possible API methods to eventually create a Discord bot that allows players to ask about the players that they are up against - hence the name AskSummoner. 

Most of the inspiration that I got from creating this application, was in part due to the fact that I used third party resources when playing the game (no, it wasn't for cheating, but an app known as Blitz). Blitz contained features in 'champion select' that would describe the players on your team and players on the other team. I knew that these minimal descriptons were true and relied on a data to support it. Though, AskSummoner aspires to do the same thing that Blitz and other programs do, I was very interested in trying it as well as well as learning more about Python in the process.

## Functionality of the Application

- [x] Allowed to search summoners
- [x] Find all their ranks in solo/duo queue and flex queue
- [x] Find their most played champions based on mastery
- [x] Display most recent match history
- [x] Implement as Discord bot
- [x] Differentiate the average of all KDA on a champion to most recent games of that champion KDA

## Problems that I ran into

In working with the API and gathering necessary information for the bot, I realized that the Match API that Riot supplies is very faulty with their matchlist parameters. What this means is that when you enter a specific season for the matchlists, much more matches are brought back in the response. As a result, I realized that this information can be gathered from an existing source (AKA op.gg). Though they managed to gather all the proper information from Riot's API to show the correct matchlists, it makes more sense to rely on the information that they had already gathered. With op.gg's information on a summoner's champion KDA, I still will have to use Riot's Match API in determining whether the summoner has improved their plays with their champion.

## Things to add in the future

- [ ] Calculate average rank in recent matches
- [ ] Determine most played champ of recent history

## Things to create after all API features are covered

- [ ] Implement as web application

