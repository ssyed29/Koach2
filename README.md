# KOach2
#Fighting Game AI Bot

Instructions for Agent-GPT to automate the completion of the application.
1. Agent-GPT can only open and edit the following python files: 'video_analysis.py', 'learn_characters.py', 'app.py'. If it is necessary to analyze the other python files, only read permission is being provided.
2. Agent-GPT can open and edit all of the .html, .css, and .js files
3. Agent-GPT must read the description of the following files in order to understand the relations between each of the files and be able to improve upon them: 
		a) app.py
			-Description: The app.py file is the main application file that contains the core logic, routes, and database configurations for the KOach2 application. This file is responsible for initializing the Flask app, setting up the database, and defining the routes for various pages within the application.
			-Associated HTML files: 
				index.html: The home page of the application, which displays a list of characters and allows users to navigate to other sections of the app.
				frame_data.html: A page that displays the frame data for a specific character, including startup frames, active frames, recovery frames, and frame advantage.
				matchup_guide.html: A page that provides a detailed analysis of character matchups, outlining strengths, weaknesses, and strategies for each character against others.
				video_analysis.html: A page that allows users to upload and analyze gameplay videos, providing insights on character performance and areas for improvement.
		b) learn_characters.py
			-Description:
			The learn_characters.py file is a script that handles character data input, editing, and deletion. It includes functions for adding new characters to the database, updating existing characters with new information, and removing characters from the database as needed.
			-Associated HTML files:
				index.html: The home page of the application, which displays a list of characters and allows users to navigate to other sections of the app.
				frame_data.html: A page that displays the frame data for a specific character, including startup frames, active frames, recovery frames, and frame advantage.
		c) video_analysis.py
			-Description: The video_analysis.py file is responsible for handling the video analysis functionality of the KOach2 application. It contains functions for uploading videos, extracting frame data from video clips, and providing insights on character performance and areas for improvement.
			-Associated HTML files: video_analysis.html: A page that allows users to upload and analyze gameplay videos, providing insights on character performance and areas for improvement.
4. Agent-GPT must download the following pre-trained AI model file using this link, then place the file in the following file path: KOach2 (project folder) -> app -> models (folder)-> frozen_east_text_detection.pb https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb
5. Agent-GPT must ensure that the appropriate libraries are installed and that the paths to each file are correctly repositioned where needed.
6. Agent-GPT must ensure that the following features are implemented into the application; Agent-GPT may install additional libraries if necessary in order to implement these features, or create new files if necessary to make the application code more modular and easy to track:
	-Update data model for users (include account types, membership settings, and preferences)
	-Implement onboarding process (questionnaire, magic sorting hat, etc.)
	-Add supported games and characters to data model
	-Implement character selection and matchup analysis
	-Create in-depth matchup guide feature
	-Implement a robust AI chat feature 
	-Update dashboard and profile UI to include progress, character usage, and preferences
	-Implement search options
	-Update app settings (themes, appearance, text size, notifications, etc.)
	-Add social features (friend requests, leaderboards, Discord integration, etc.)
	-Create resources section with glossary and tutorials
	-Implement contact and support options
	-Update premium features (advanced matchup analysis, training regimens, etc.)
	-Add game-specific pages with tabs for mechanics, updates, and notifications
	-Implement username and password registration for creating accounts
	-Implement account management (payment, cancellation, profile deletion) - focus on this later
	-Implement all of these features for the following games: Tekken 7, Mortal Kombat 11: Ultimate, Street Fighter 6, Dragon Ball FighterZ, The King of Fighters XV, Guilty Gear Strive, Melty Blood: Type Lumina Ultimate Marvel vs Capcom 3
	-Allow for the developer to regularly add more games over time (content update process)
	-Implement character roster for each game
	-Implement character archetype-based suggestions
	-Integrate AI-generated matchup breakdown
	-Create a view for app appearance customization
	-Implement regional leaderboards and active player count for supported games
	-Add Discord integration for voice chat (optional)
	-Implement game trailers and optional update push notifications if the user opts to receive them
	-Handle account deletion with 30-day deactivation period
	-Display "Coming Soon" text for unreleased games

5. Additional Goals for Agent-GPT for this application:
	-Goal 1: Develop a mobile and web application using Python/Flask/RESTful API as the backend, and HTML/CSS/JavaScript for front end development. This app serves to help users learn and improve their fighting game skills based on an initial profile analysis of the user's current skill level at fighting games, prior fighting game experience, preferred play style, and knowledge of fighting game terminology/lingo. Save your progress frequently so that when I re-initialize Agent-GPT, the next agent can pick up from where you left off.
	-Goal 2: The AI will develop in-depth knowledge of the following fighting games: Street Fighter 6, Tekken 7, Mortal Kombat 11: Ultimate, Dragon Ball FighterZ, The King of Fighters 15, Guilty Gear Strive, Melty Blood: Type Lumina, and Ultimate Marvel vs Capcom 3. The AI will learn the following for each game: in depth knowledge of the game mechanics, character roster, move list, frame data for each character's moves, in depth matchup knowledge for each character so that the AI can teach the user what the best strategy is to use against the opponent character based on the character that the player wants to use and improve with. For example with Tekken 7, the AI should categorize the movelist by the following attack types: throw attacks, punish attacks, low attacks, mid attacks, high attacks, homing attacks, tracking attacks, power crush attacks, wall bounce attacks, crushing attacks (high or low), evasive attacks, etc. Give priority to Tekken 7 and Guilty Gear: Strive first before proceeding to gather the data for the rest of the games
	-Goal 3: you will implements the following features into the application: user registration and authentication, security settings, video analysis, in-app payment handling, game and character selection, matchup analysis, a full character database with character breakdowns that highlight the character's overall gameplan, strengths, weaknesses, etc. The application must also build upon video_analysis to create a fully featured video playback analysis feature where the AI learns and records gameplay data to then present the user with feedback.
	-Goal 4: you will build upon a chat feature where the user can speak and interact with the AI. The AI will first learn about the user's preferences and knowledge, then develop goals and challenges for the user to develop their skills. The AI should speak with the user at a level that is appropriate for their level of skill and knowledge of fighting games and terminology. The user should be able to ask about each game, character and character matchups, and the AI will provide detailed responses relevant to the query and application.
	-Goal 5: The program must have appropriate progress tracking and data storage to remember the user’s profile. The AI should be able to update the user's skill levels dynamically based on changes to the user's performance using specific characters and learning how to counter certain moves from the opponent's moveset that are considered to be challenging. The AI must be encouraging to the user and be willing to teach the user whatever the user wants to know about the specific fighting game.
