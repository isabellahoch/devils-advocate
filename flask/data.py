# -*- coding: UTF-8 -*-
articles = []
articles.append({"title":"Parasite: Best Movie ever?",
	"formatted_title":"<span style='font-style:italic'>Parasite</span>: Best Movie Ever?",
	"section":"A&E",
	"edition": "February 2020",
	"author":"devin-leung",
	"img":"https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_UY1200_CR90,0,630,1200_AL_.jpg",
	"contents":"&nbsp;&nbsp;&nbsp;&nbsp;If your head has been anywhere near the entertainment industry within the past few months, you most likely would have heard of the extremely popular Korean film, <span style='font-style:italic'>Parasite</span>. Having been nominated for numerous awards including at the upcoming Oscars (update: It won Best Picture!) and having won numerous awards such as Best Foreign Language Film at the 2020 Golden Globe Awards, this movie is definitely one you shouldn’t miss out on. The endless action as well as unexpected twists keep you at the edge of your seat. In addition, the social message and articulate imagery throughout the film are very compelling and relevant to today's society.<br>&nbsp;&nbsp;&nbsp;&nbsp;Directed by the talented Bong Joon-Ho, this film sucks the viewer into the world of the low-class Kim family living in the suburbs of Korea. Living in a semi-basement house and folding pizza boxes for money, this movie highlights their struggle for success. They soon meet the wealthy Park family and attempt to take advantage of them in order to raise their own socioeconomic status. Throughout the story’s timeline, many secrets are revealed as both families are oblivious to each other’s motives. As David Edelstein from <span style='font-style:italic'>Vulture</span> said, “What keeps you rapt in Parasite is the visual wit — every shot distills the movie’s themes — and the richness of the characters and performances.” Each frame is meticulously crafted to make this movie a pleasant masterpiece.<br>&nbsp;&nbsp;&nbsp;&nbsp;Personally, I would recommend going into the movie with no expectations. Therefore, you can experience the story unfolding before your eyes, without any preconceived notions. Also, don’t let the fact that this film is in Korean deter you. As Bong Joon-Ho said in his Golden Globes acceptance speech, “Once you overcome the one-inch tall barrier of subtitles, you will be introduced to so many more amazing films.” Furthermore, I would recommend watching the film twice because of all the easter eggs and hidden messages. Watching a second time will definitely give you many “ah-ha” moments of references you didn’t catch the first time. One piece of advice I would give is to pay close attention to detail and symbolism when watching, not only to the images and objects in the film, but also to how the camerawork is done. This will reveal a lot about the underlying critique of social class in today’s society. Don’t worry, if you still don’t get some of the references, there are always many YouTube videos explaining the movies. Just don’t go down a rabbit-hole of Parasite explanation videos.<br>&nbsp;&nbsp;&nbsp;&nbsp;So if you haven’t seen Parasite yet, hurry, before it leaves theaters. I can guarantee you will enjoy it!"
	})

articles.append({"title":"Native American Appropriation in the Super Bowl",
	"section":"Sports",
	"edition": "February 2020",
	"author":"zach-beischer",
	"contents":"&nbsp;&nbsp;&nbsp;&nbsp;It has been over a month since the 54th Super Bowl, in which the Kansas City Chiefs won their first Super Bowl in 50 years. The Chiefs, however, are part of a group of professional sports teams who continue to receive backlash for their cultural appropriation of Native American’s through their team name, logo, traditions, and fans. Some other teams that also fall in this group are the Washington Redskins, the Atlanta Braves, and the Cleveland Indians to name a few. While the racist names and logos of these teams often receive deserved attention, the actions of fans of these organization can often be overlooked. Aside from wearing offensive headdresses and face paint, fans for many of these teams participate in the well-known tomahawk chant. While I had seen many teams’ fans do this chant, I admittedly did not know the origin of the chant, but was able to get some facts with a little research.<br>&nbsp;&nbsp;&nbsp;&nbsp;The tomahawk chop chant is said to have originated from Florida State University, whose mascot is the Seminole. A former Florida State University president once claimed that the chant originated from the school’s marching band in the 1980s. For a while, the mascot for the school was “Seminole Sammy,” a white student dressed up in fake, stereotypical Native American dress. The chant is also said to have been brought to professional sports by Deion Sanders, a football hall of famer. However, he first brought the chant to baseball in the 1990s, when he was a member of the Atlanta Braves, a team that currently has a tomahawk in their logo. According to multiple sources, there is no indication that Native Americans ever made the tomahawk chant gesture, but rather that it was made up by white people appropriating their culture.<br>&nbsp;&nbsp;&nbsp;&nbsp;On another note, the tomahawk chop has not only been restricted to sports. For example, in 2012, members of Massachusetts Senator Scott Brown’s staffers were caught on video using the chant to mock his then opponent, and current presidential candidate, Elizabeth Warren’s, Native American ancestry.<br>&nbsp;&nbsp;&nbsp;&nbsp;The tomahawk chant is just another example of a way that Native American culture is incorrectly represented and used by others in America. Many fans who participate in this chant at games probably have no knowledge of the history of the chant or even an accurate history of Native Americans. Like the creator of this chant, many of these fans are non-native. As previously mentioned, the names, logos, and even mascots of teams like the Chiefs can overshadow offensive fan behavior."
	})

all_articles = {}

for article in articles:
	if not "formatted_title" in article:
		article["formatted_title"] = article["title"]
	new_id = ""
	for character in article["title"].lower():
		if character.isalnum() or character == " ":
			new_id += character
	new_id = new_id.replace(" ","-")
	article["id"] = new_id
	all_articles[new_id] = article