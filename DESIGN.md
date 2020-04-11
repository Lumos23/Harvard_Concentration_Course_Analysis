Before writing html code for our project, we first acquired the data in excel format, changed it to txt and then into database format.

As a first step in using our website, we want to implement a feature let our users select their intended concentration.
In order to put all possible concentrations as options in the drop-down select form, we query for all distinct names of major, and set them as options for the form.
Then we use a selection form to ask the user for number of classes he or she has taken.
In order to provide the exhaustive list of possible classes a user may have taken, we did another “distinct query”, and iterate it for n times, where n equals the number of classes a user has taken.
We combine these selections into one div instead of multiple, so that when the user clicks submit, all information can be submitted at once.
There is also a link available to the user that will take them to my.harvard where they can look up the official titles of their courses if need be.
After submitting the classes, these classes are stored inside a list so that it can be used later for similarity test.
In the process we also made use of session to store the information of concentration and number of classes that the user entered, so that we can access it easily in later code.


Our idea of finding the most similar profiles and most frequently taken classes of these students is based on comparing lists of classes using the Jaccard index, which is essentially comparing the percentage of union in the sets.
We put the information in the existing database into a dictionary, where the key is the person id (for those who declared this concentration) and value is the corresponding classes.
Then we compare the list of classes from the user input and all the lists of classes we generate from the subset of our database, and keep track of the highest j values as well as their corresponding ids.
Then we put all classes these past students in the concentration with the top-ten j value took in a master list, and find the frequency of each distinct class in the list.
We store this information in a dictionary so that there would be a clear correspondence between class and the frequency of the class.
After getting this dictionary, we sort it by the frequency of the classes, and take the top ten.
Another feature we have in the result section is showing the user a most-similar profile.
We display all the classes, this is done by creating a variable called profiles, which is essentially a list of lists.
Elements in profiles are the lists of classes students with the highest j value took (which can be acquired by referring back to the our dictionary earlier).
To display these classes, we write for-loops in our classes.html to show these classes line-by-line.