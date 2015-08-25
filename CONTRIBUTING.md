# Contributing

Contributions are welcome and greatly appreciated! Please review the rules below before submitting a pull request.

## Rules for content

Content is written in markdown format. If you add new information, please provide a source, in case of Web pages add a link to the source and respect copyright.

Sources should be trustworthy, which is obviously a subjective assessment. Please use common sense and don't try to promote sites, that are only made for advertising.

### General rules

* Filenames for are all lowercase, words are separated by hyphens.
* Header fields are provided in alphabetical order.
* The body text goes after the 2nd `---`.
* The following header fields are supported for all content types:
    * `created`: date and time of content creation, e. g. `2015-08-25 13:30:07`. If you edit an existing page, don't change this value.
    * `description`: A short summary of the content.
    * `title`: Title of the document.

### Exercise rules

* All exercise are in the [Exercise directory](https://github.com/calisthenics/site/tree/master/content/exercise).
* Exercise names are in singular form unless that is ungrammatical.
* The following header fields are currently supported for exercises:
    * `groups`: List of exercise groups, e. g. [Push, Push Up].
    * `muscles`: List of muscles trained by the exercise. `[Deltoids, Trapezius]`.
    * `template`: `exercise.html`
    * `variants`: A list of exercise variations, e. g. `[Crunch, Jack Knife]`.

### Muscle rules

* All muscles are in the [Muscle directory](https://github.com/calisthenics/site/tree/master/content/muscle).
* Currently muscle names are not consistent regarding number (singular, plural). Please help finding a sensible rule here.
* The following header fields are currently supported for muscles:
    * `template`: `muscle.html`