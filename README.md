kore_GSheet
===========

The scripts I am using to find and fix errors in the Optimized Core 2k/6k deck ([courtesy of Nukemarine from the RevTK forums](http://forum.koohii.com/viewtopic.php?pid=95122#p95122)). It's also what I use to maintain parity between [my Core 2k/6k anki deck](http://forum.koohii.com/viewtopic.php?pid=177610#p177610) and the [main Google Spreadsheet](https://docs.google.com/spreadsheet/ccc?key=0AscWM0WNU3s4dHE3R0M0VG5JMndrMEpiNTdnRjhtYnc#gid=0) from which new versions of that deck are ultimately generated. (That is, I sync between the two using the Google spreadsheet API).

This is mostly throwaway code, which explains why it's so hideous (I did a copy+paste every time I needed a new function. Contain your derision, please!). There's really no use for it after the deck has been cleaned and the updates pushed to the main spreadsheet (which I've done now).

The code that talks to the Google Spreadsheet can serve as a useful reference in the future. Unfortunately, Google Spreadsheets have proven to be somewhat unwieldy for this task (even more so for such a large spreadsheet -- it's so slow!). In the future, it'd be nice to create some resource to provide an online service for collaboratively editing anki decks that can then generate and/or sync actively used decks (unless anki2 does something like that already, I'm not too sure).