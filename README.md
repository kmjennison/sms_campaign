# SMS Campaign Manager

A simple way to create an SMS Campaign for NGOs.

Many people have access to text messaging but no access to internet, making texts an important method of communication for NGOs with a wide variety of applications. For example, text message reminders for taking medication on a schedule significantly improves adherence (http://www.ncbi.nlm.nih.gov/pubmed/22554973).

However, setting up text message communication systems generally requires an NGO to hire a developer, which is expensive and time-consuming.

Here, we provide an easy graphical interface for setting up text reminders. The interval of recurring reminders is customizable for each reminder "campaign" (e.g. each medication), and you can enroll people in a campaign via SMS. People can respond to SMS reminders to indicate they've completed a task (e.g. taken their medication).

![screen shot 2014-05-04 at 11 06 27 am](https://cloud.githubusercontent.com/assets/5600355/2873673/ea382c46-d3b6-11e3-93ce-9e3abe3643ea.png)

SMS Campaign Manager is an app built on Django, the Twilio API, and a Bootstrap front-end.

## Set Up

Here's how to get going with your version:

Clone the repository from GitHub - in your terminal/command line type

`$ git clone https://github.com/kmjennison/sms_campaign.git`

`$ cd sms_campaign`

TODO add instructions on how to install, configure, & run etc

## TODO

- Make reminder scheduling more flexible, beyond just a recurring interval
- Create custom messages per reminder (for example, if the second reminder needs a different message than the first)
- Create a customizable callback function when a user responds to a text reminder
- Make group signup form and handle authentication
- Require Twilio API keys per group (so they can handle payment)
- Style Django admin

## Contributing

### Contributing code

- Fork the repository.
- Create a branch (e.g. `my-awesome-feature`) for the work you’re going to do.
- Make your awesome changes in your topic branch.
- Send a pull request from your branch to this repository.

### Other ways to contribute

- Try the project out yourself!
- [File issues](https://github.com/kmjennison/sms_campaign/issues/new) about bugs,
  problems, or inconsistencies you run into.
- [File issues](https://github.com/kmjennison/sms_campaign/issues/new) with suggestions,
  feature ideas, or UI mockups for improvements.
- Read through the documentation (just this README for now), and look for ways
  it could be improved. Click "Edit" on [the file](https://github.com/kmjennison/sms_campaign/blob/master/README.md)
  and make the changes yourself if you can!


## Authors

Made with <3 by [@lzecon](https://github.com/lzecon), [@oahzit](https://github.com/oahzit), [@secondbreakfast](https://github.com/secondbreakfast), [@kmjennison](https://github.com/kmjennison), Amy King, [@alysonla](https://github.com/alysonla), & [@jignab](https://github.com/jignab) at #hackbrightforgood, May 3-4, 2014
