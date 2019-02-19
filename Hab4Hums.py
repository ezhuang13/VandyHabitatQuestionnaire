# ----- Set these parameters on your own!! You may have to tweak things for future use ----- #

# Number of ranked questions (should be at end of questionaire)
numRankedQs = 5
# Boolean if venmo is included as end question
removeVenmo = True
# Names of files
inputFile = "2019.txt"
outputFile = "2019Results.txt"

# Note: I usually replace the csv Google forms generate with a txt file, replacing all commas with tabs.
# Frankly I don't remember why I did that. It's probably not needed. Feel free to experiment on your own :D
answerDelimiter = "\t"


def sort_diffs(item):
    return item[1]


class Participant:
    def __init__(self, name, grade, email, answers):
        self.name = name
        self.grade = grade
        self.email = email
        self.answers = answers

    def get_top_matches(self, people, grade=False):
        multiple_choice_diffs = self.calculate_diffs(people, grade)
        num_matches = 0
        top_matches = []
        for key, value in sorted(multiple_choice_diffs.items(), key=sort_diffs):
            if num_matches == 25:
                break
            top_matches.append([str(key[0]), str(key[1])])
            num_matches += 1
        num_matches = 0
        low_matches = []
        for key, value in reversed(sorted(multiple_choice_diffs.items(), key=sort_diffs)):
            if num_matches == 25:
                break
            low_matches.append([str(key[0]), str(key[1])])
            num_matches += 1
        return top_matches, low_matches

    # Difference is either 2 (different) or 0 (same), for ranking it is the difference
    # Return: dictionary containing: (key, value) = (email, total diff)
    def calculate_diffs(self, people, grade):
        mc_diffs = {}
        # Populate keys
        for person in people:
            if grade and person.grade != self.grade:
                continue
            if person.email == self.email:
                continue
            mc_diffs[(person.email, person.name, person.grade)] = 0
        # Populate list of answers
        for i in range(len(self.answers)):
            for person in people:
                if grade and person.grade != self.grade:
                    continue
                if person.email == self.email:
                    continue
                if person.answers[i] != self.answers[i]:
                    if type(person.answers[i]) == str:
                        mc_diffs[(person.email, person.name, person.grade)] += 2
                    else:
                        mc_diffs[(person.email, person.name, person.grade)] += abs(person.answers[i] - self.answers[i])
        return mc_diffs


# ----- Read in input --------
# Saved it as a utf8
with open(inputFile, "r", encoding="utf-8") as csvFile:
    data = csvFile.readlines()

# Read in the data
# Formatted: data[person][value]
for i in range(len(data)):
    data[i] = data[i].strip().split(answerDelimiter)
    data[i] = data[i][1:]
    # Remove venmo
    if removeVenmo:
        data[i].pop()
    # Work backwards and convert all numeric question answers to ints
    for j in range(1, 1 + numRankedQs):
        data[i][-j] = int(data[i][-j])

# Create all participants
participants = []
for line in data:
    participants.append(Participant(line[0], line[1], line[2], line[3:]))

# Get matches for each participant and write results
f = open(outputFile, "w")
for participant in participants:
    info = []
    top, low = participant.get_top_matches(participants)
    topGrade, lowGrade = participant.get_top_matches(participants, grade=True)
    info.append("NAME: " + participant.name + "\n")
    info.append("EMAIL: " + participant.email + "\n")
    info.append("TOP MATCHES IN GRADE:\n")
    for i in range(25):
        info.append(str(topGrade[i][0]) + ", " + str(topGrade[i][1]) + "\n")
    info.append("LOWEST MATCHES IN GRADE:\n")
    for i in range(25):
        info.append(str(lowGrade[i][0]) + ", " + str(lowGrade[i][1]) + "\n")
    info.append("TOP MATCHES OVERALL:\n")
    for i in range(25):
        info.append(str(top[i][0]) + ", " + str(top[i][1]) + "\n")
    info.append("LOWEST MATCHES OVERALL:\n")
    for i in range(25):
        info.append(str(low[i][0]) + ", " + str(low[i][1]) + "\n")
    info.append("\n")
    f.writelines(info)
f.close()
