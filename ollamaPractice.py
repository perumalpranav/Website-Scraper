import ollama

models = ollama.list()
model_name = 'deepseek-r1:8b'

modelAvailable = False

for m in models['models']:
    if m['model'] == model_name:
        modelAvailable = True
        break

if not modelAvailable:
    answer = input(f"The model that is used in this code {model_name} is NOT on your device, would you like to install it? (Y/N)")
    if answer != "Y":
        raise RuntimeError(f"Model \"{model_name}\" not found. Halting execution.")


content = """
Chapter 1: Awakening Memory

The streets glowed with neon lights, and scantily-clad ladies strolled by, alongside traffic lights at the zebra crossing, and out-of-control dump trucks...


Beep~~


A sharp horn pierced through the dream, and Tao Yu woke up from his sleep, sweating profusely and gasping for breath.


A faint musty and sweaty odor entered his nostrils with each breath, gradually bringing Tao Yu to his senses.


It was happening again, the same dream, so vivid that he couldn't distinguish between illusion and reality.


Whether he was Tao Yu, the social animal from the twenty-first century, or Tao Yu, the nearly eighteen-year-old from the outer city, he was starting to lose track.


Over the years, he had occasionally had this dream, but as the eighteenth birthday, representing the day of awakening, drew nearer, the dreams became more frequent, and in the past month, they occurred every time he closed his eyes.


At first, he thought it was just stress and hallucinations as the day of awakening approached, but with more memories and information, the systematic and coherent memories and knowledge told him it was all real.


According to those novels in the memories from his dreams, it should be a reincarnation to another world...


Thinking back to the peaceful, warm, and beautiful world in his memories, and then looking at the damp bed made of bricks and planks, looking up at the stained asbestos wall, and the windows patched with cardboard.


Tao Yu's expression became somewhat vacant.


Through the gaps in the cardboard over the window, he watched the pitch-black outside, listened to the wind in the darkness, and heard some faint murmurs and vague whispers, making Tao Yu's feelings even more complicated.


There was an old oil lamp on the bedside table, its flame the size of a soybean, casting a hazy light over the small room. But all the light stopped abruptly at the window, as if unable to penetrate outside.


The occasional flicker of the flame made the shadows in the room shake, as if coming to life, and it seemed as though the tiny flame could go out at any moment.


"Is there really a peaceful world where everyone can eat meat..."


Having lived in this world for eighteen years, the memories of his past life, so taken for granted, now seemed as if from another lifetime.


The things he considered normal and natural in his past life were complete luxuries, mere wishes, in this life!


Why couldn't it be him from this world who had traveled to that one?


With all the combat and survival skills he had practiced relentlessly over the past eighteen years, he would have at least been a bodyguard or a live-in son-in-law in the metropolis of the twenty-first century.


Abyss...


The Sword of Damocles hanging over everyone's head in this world, the end of the endless realm.


No one knew how many years had passed since the world caught the attention of the Abyss.


From the limited knowledge Tao Yu had, he gathered that when the Abyss first began to consume the world, the world's will awoke instinctively, granting all people the power to resist the Abyss.


It was through Pioneers venturing into the fragments of worlds within the Abyssal Rift, seizing Yuan Force to prolong the world's existence, that life had continued to this day.


As for what exactly had happened over the years, Tao Yu didn't know, but the grey fog that symbolized the Abyss's invasion had already spread across the world, squeezing human habitats into a succession of cities and shelters.


The connections between cities were mostly severed, and it was only with the Lamp of Will illuminating the path through the grey fog that one could move forward with difficulty, maintaining increasingly scant exchanges.


The Flame of Civilization that dispels the fog in each city and the day of awakening on everyone's eighteenth birthday seemed like the last gifts left by the will of the world...


Giggle, giggle~


A distant crowing of a rooster came from the pitch-black outside, as if in an instant, all the darkness disappeared, revealing a dim light.


The crowing brought Tao Yu out of his reverie as well, and looking at the dim light outside the window, he couldn't help but heave a sigh. Then he reached over to twist the oil lamp stained with black oil at the head of the bed, extinguishing the soybean-sized flame.


Lately, there had been more and more disappearances in the outer city, and it was unclear when an end would come. He hoped that on today's day of awakening, he would successfully awaken a combat talent. Considering his parents' gifts, the best talent he could possibly awaken was likely Dynamic Vision.


If the grade of Dynamic Vision could reach Grade C or higher, perhaps his status could change.


Putting on plastic-bottomed shoes stained with an unknown black grime, Tao Yu pushed open the creaking old door. Outside was a living room similar in style to his own room.


The living room walls were mainly patched together with asbestos boards and iron sheets, and in the middle stood a table spattered with rust, composed of three tripods. The several stools in the living room also varied in style, as if they were cobbled together from various scraps of material—wooden, triangular, metallic, all sorts.


Approaching the water tank, Tao Yu picked up a porcelain basin and scooped up a basin of water using a rugged aluminum alloy ladle.


Looking at his reflection, a slender face with a touch of delicate features, Tao Yu felt a tangle of emotions.


He wasn't bad looking, it just seemed that he was malnourished. The high frequency of dreams this month had started to merge his thoughts more and more with those of his previous life, making his mind feel much sharper.


Squeak~


The same grating sound of a door opening rang out, and a dark-skinned, capable-looking woman stepped out of the room. She saw Tao Yu and smiled, showing her white teeth.


"Ah Yu, today is your Awakening Day. You should rest well. I'll take care of the farm work."


"Sister-in-law, I can't sleep."


Tao Yu politely nodded to the woman, then reached out to wash his face.


"Alright. Mom and Dad should be returning by noon today. They should be able to bring you some useful weapons and equipment."


The woman sighed, thinking Tao Yu was too anxious, so she comforted him with a few words.


"I'll go get some fresh stuff for you to eat on the first day."


"Thank you, Sister-in-law."


Tao Yu finished washing his face and voiced his gratitude.


By count, this was his third sister-in-law. His eldest and second brothers had both died on their Awakening Day, his fourth sister was married off, his fifth brother died on a cannon fodder mission, and his sixth sister went mad and was killed by the security force. Besides himself, only his parents, his third brother, third sister-in-law, and his sixteen-year-old younger brother were left in the family.


To lower the priority of the cannon fodder quota and to improve their own weight allocation, his parents had recently been considering having a ninth child, but it was uncertain whether they could still bear one.


Although because both of his parents had relatively stable jobs, he had lived a 'relatively stable' life since childhood, he had become accustomed to life and death from a young age.


Since the beginning of the Abyssal invasion, the world will had awakened and bestowed upon people the power to fight back. The Awakening Day was a turning point of utmost importance for everyone.


From the day of awakening, everyone in this world needed to spend some time delving into The Abyssal Rift to search for Yuan Force to strengthen themselves, which also helped to fortify the world will against the Abyssal invasive forces.


It wasn't about being datafied or panelized, but the world will would enable individuals to understand their abilities more clearly after the Awakening Day and accelerate their empowerment through Yuan Force, while also awakening their personal talents.


Individual talents were myriad and strange, most of which were of little help in combat, greatly affecting the speed of personal growth.


Due to the problem of limited resources, talents inclined towards combat were more likely to receive training and certain privileges and resources from the companies.


For instance, Tao Yu's father, Tao Long, possessed the talent Eagle Eye (Grade C+). Although it was of limited help in direct combat, it gave him certain advantages in roles like scouting, sniping, and reconnaissance, allowing him to survive many years.


His mother, Hong Xia, had the talent Dexterity (Grade F), theoretically more suitable for combat than Eagle Eye, but her innate grade was too low, only slightly better than the lowest F-.


Although there were cases of people improving their talent grades and even transforming or having multiple talents, such occurrences were clearly impossible for an ordinary family.


Therefore, his mother chose to marry his father, hoping to cultivate the more suitable standard combat talent Dynamic Vision.


She opted to specialize in a manufacturing Skill, her dexterous hands earning her a position as a senior skilled worker in a leather factory.


Coupled with the weighting boost from birthing many children, they had not been assigned cannon fodder tasks by the company over the years.


Although individual talents had a not insignificant relationship with heredity, among Tao Yu's many brothers and sisters, only his third brother, Tao Tong, had inherited the optimized talent from their parents, acquiring Dynamic Vision (Grade D+).


Theoretically, he could have achieved even more, even joining the company's security force at one point.


But after losing both legs on a mission, everything came to an abrupt halt.


Whether it was items for regenerating limbs or mechanical prostheses that would allow him to continue fighting, none were affordable for the family.


Fortunately, since he was injured on a mission for the company, the company 'generously' exempted him and his wife, Li Li, from the cannon fodder quota for life, forever free from the worry of being forcibly drafted for such tasks...

"""

response = ollama.chat(
    model='deepseek-r1:8b',
    messages=[
        {
            "role": "system",
            "content": (
                "You are a novel editor. Your task is to improve the sloppy machine tranlated English "
                "generated from Chinese text. Make the English natural, fluent, and faithful to the meaning in Chinese. "
            )
        },
        {
            "role": "user",
            "content": (
                f"Machine Translated English: {content}"
            )
        }
    ]
)

print(response['message']['content'])
