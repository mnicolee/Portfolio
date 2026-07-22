Rewrite the text under each ⟦marker⟧ so it sounds like a real, warm person wrote it, not AI. Rules:
- Keep every ⟦marker⟧ line as-is, same order; rewritten text under it. Return only that.
- Keep all facts, names, numbers, links, and the **bold**/*italics* emphasis.
- NO em dashes (—). No "notable". Don't make it peppy or salesy.
- Similar length or a bit shorter.

I'm Nicole, a computational behavioral neuroscientist.

(Remaining pages only. Already-applied pages, and the DABEST page, are not here.)

---

## HOME (index.qmd)

⟦home.herosub⟧
Computational behavioral neuroscientist & hardware tinkerer

⟦home.about.p1⟧
I'm a **neuroscientist** in the ACC Lab (Adam Claridge-Chang) at Duke-NUS Medical School, where I completed my PhD and now continue as a Research Fellow, **building optogenetic methods to study how small circuits in the *Drosophila* brain shape behavior.**

⟦home.about.p2⟧
Before the flies, I completed my B.S. in Biochemistry at the University of Washington, Seattle, and worked on several projects: the biochemistry of collagen degradation, mTOR and kappa-opioid receptor signaling, asymmetric cell division, and cancer drug-resistance. Outside the lab, I paint 🎨, play games 🎮, and build apps 📱.

⟦home.three.neuroscience⟧
**Optogenetics for behavioral neuroscience**, developing and applying light-driven tools to manipulate neural activity, including potassium channelrhodopsins and opto-GPCRs.

⟦home.three.hardware⟧
**Experimental hardware design**, designing and prototyping custom rigs and hardware components for optogenetic stimulation and behavioral experiments.

⟦home.three.numbers⟧
**Estimation statistics**, contributing to DABEST for effect sizes and confidence intervals over p-values. Building open-source Python packages for **data analysis and visualization**.

⟦home.news.viset⟧
An nbdev Python package on GitHub for itemizing and comparing sets, not just viewing them interactively.

⟦home.news.opn3⟧
A light-activated GPCR that switches neuromodulatory signaling on and off, so we can dissect how specific circuits in the brain shape behavior.

⟦home.news.celegans⟧
A DIY behavior rig: custom arena, controlled illumination, camera, and a tracking pipeline for freely moving worms.

---

## RESEARCH (research.qmd)

⟦research.lead⟧
How circuits and internal states shape what an animal does, and the light-driven tools I build to switch those circuits on and off in the fly brain.

⟦research.card.neuralcircuits⟧
A large-scale optogenetic and behavioral ethomics study of how brain circuits shape movement in *Drosophila*, forming the core of my PhD thesis.

---

## CONTACT (_contact.qmd — currently hidden)

⟦contact.intro⟧
Have a question, a collaboration in mind, or just want to say hello? Drop a note below and it'll come straight to my inbox.

---

## PAPER — Valence / thesis (papers/valence/index.qmd)

⟦valence.p1⟧
My PhD thesis work. Using an optogenetic screen of the mushroom body output neuron (MBON) split-GAL4 library, I applied bidirectional manipulation, activating and silencing defined MBON populations, across two custom-built behavioral assays. The MBONs are the output layer of the mushroom body, the fly's center for learning and memory, and are widely treated as carrying the "value" (reward vs. punishment) of a stimulus.

⟦valence.p2⟧
The screen was designed to separate two things that are easy to confound: the *valence* a circuit assigns and the *locomotion* it drives. By reading behavior across both assays, the work maps where, and how, these two signals become entangled in *Drosophila* circuits.

---

## HARDWARE — C. elegans rig (hardware/celegans/index.qmd)

⟦celegans.intro⟧
This rig was built for the *C. elegans* arm of the KCR silencing study, where I needed to record and quantify worm locomotion during optogenetic stimulation. No *C. elegans* behavioral lab existed locally, and dedicated worm-tracking systems would have been cost-prohibitive, so I **built the whole setup from a stereoscope and a camera**, designing and 3D-printing the parts that did not exist. This was done in collaboration with the Duke-NUS 3D Printing & Prototyping (3DPP) Lab; credit to Dennis Ong, who brought the fabrication and 3D-printing expertise that made the ideas real.

⟦celegans.base⟧
The base chamber holds the worm arena, the agar, and the optics in a fixed, repeatable geometry. Cutting each piece separately and joining them magnetically made the build modular: worn or damaged parts could be replaced individually rather than re-machining the whole assembly.

⟦celegans.arenas⟧
Individual worms were placed in 3.5 × 3.5 mm arenas cut into a 51 mm-diameter transparent acrylic disk, seated on NGM agar in a 60 mm Petri dish. The confined geometry kept worms in frame, physically isolated individuals to prevent crossing or mating (both of which confound tracking), and let me stage several animals at once while imaging them one at a time.

⟦celegans.camera⟧
Images were acquired at 29 FPS with a FLIR Grasshopper3 near-infrared camera on an Optika stereomicroscope at 1.5× magnification. We needed to fix the camera to the microscope securely, so I designed a custom C-mount adapter and had it 3D-printed. The rigid mount eliminated camera displacement during recording.

⟦celegans.rig⟧
The whole setup sat inside a temperature-controlled incubator. Constant 850 nm infrared LEDs lit the arena for recording without activating the opsins. Optogenetic stimulation used green (530 nm) and blue (460 nm) LEDs on heatsinks. Each 30 fps recording ran 10 s of darkness, then 10 s of green stimulation, then 40 s of darkness, the final window capturing the kinetics of locomotor recovery.

⟦celegans.dlc⟧
Because the low-contrast stereoscope video defeated the classical trackers I tested, I trained a custom DeepLabCut model on our own footage. Videos were down-sampled to 512 × 512 px (a worm spans roughly 17 × 80 px); 10 key points were hand-labeled head-to-tail across 280 frames from 14 videos, and a ResNet-50 network was trained for over 500,000 iterations. A custom Python package (Celegans_tracking) then converts the key-point coordinates into baseline-normalized worm speed, with effect sizes reported via the DABEST estimation framework.

---

## HARDWARE — Climbing rig (hardware/climbing/index.qmd)

⟦climbing.intro.p1⟧
A climbing assay reads out motor function through negative geotaxis: knock a fly to the floor of a vertical chamber and it climbs, and how it climbs, its speed, height, falls and pauses, reports on the motor circuitry driving the behaviour. The classic version is done by hand: tap a vial of flies and count how many pass a line in a set time. That is enough to catch gross motor deficits, but manual tapping agitates every fly a little differently, it leaves no precise moment to synchronise light or tracking to, and a single pass-or-fail line throws away the shape of the climb.

⟦climbing.intro.p2⟧
That gap is what this rig was built to close. To measure *Drosophila* climbing under optogenetic control in my thesis, I needed to agitate every fly the same way, every trial, and hand off cleanly to timed light stimulation and frame-by-frame tracking. So I built a chamber and, around it, an automated rig that **made the startle reproducible and locked it to the optogenetics**. The pneumatic and electronics build was done in collaboration with the Duke-NUS 3D Printing & Prototyping (3DPP) Lab; credit to Dennis Ong, who built the fabrication and microcontroller side.

⟦climbing.apparatus⟧
Climbing behaviour is assessed in a custom acrylic cassette (170 × 94 × 9 mm) holding 17 individual chambers (7 W × 86 H × 3 D mm), CNC-milled into a 3 mm transparent acrylic sheet mounted onto a white acrylic diffuser (Figure 1B). One fly per lane keeps individuals in frame and physically separated, so seventeen animals can be recorded at once without ever crossing paths, and the tall, narrow geometry defines a repeatable climb. Flies are briefly anaesthetised on ice for 30 s, loaded one to a chamber, and given 3 minutes to recover before any testing begins.

⟦climbing.illumination⟧
Optogenetic stimulation can be delivered in green (530 nm), blue (460 nm), or red, with intensity adjustable up to ~20 µW/mm². The low, tunable intensities suit light-sensitive opsins requiring minimal activation. The whole assembly sits inside a temperature-controlled incubator.

⟦climbing.pneumatic.p1⟧
Every recording set starts by displacing all seventeen flies to the bottom of their chambers. I did this by hand at first, tapping the cassette down, but manual tapping introduced inconsistent delays between the flies resetting and the start of tracking and light, which is exactly the temporal precision an optogenetic experiment cannot afford to lose. So I replaced it with a pneumatic system (Figure 1D) that agitates the same way every time and hands off cleanly to the recording.

⟦climbing.pneumatic.p2⟧
The cassette mounts to an acrylic backboard via a single-acting pneumatic piston, held by 3D-printed adapters on optical posts to stay rigidly aligned and damp vibration. Compressed air reaches the piston through a normally-closed solenoid valve with a manual emergency release. An Arduino UNO (programmed by Dennis Ong, 3DPP Lab) controls actuation, with an OLED and rotary encoder to set parameters. Tracking pauses during agitation and resumes only once every fly is confirmed back on the chamber floor, since a stroke occasionally fails to dislodge one.

⟦climbing.analysis⟧
Video and positions are processed in real time by CRITTA, a tracker that segments flies from the background by subtraction, giving x–y coordinates per fly per frame. I then wrote a custom Python package, DrosoClimb, to turn those raw tracks into behaviour: it converts coordinates to millimetres, splits each trial into its dark, light and recovery phases, and classifies every frame as walking, pausing or falling. Those thresholds come from ground truth I hand-labelled in Tracker (Figure 2). From there it computes a range of climbing metrics, each reported as a DABEST effect size, together building an ethomic profile of the fly's motor behaviour.

⟦climbing.classification⟧
Every frame is scored against thresholds fixed on hand-labelled training video (17 flies, 1,810 frames, top and bottom 10% trimmed): a fall is a downward jump beyond −3.17 mm per frame, a pause is a speed below 2.588 mm/s, and anything faster without a fall is a walk. On an independent test set (13 flies, 1,477 frames) the classifier reads 92% of walking, 93% of pause and 83% of fall frames correctly.

---

## TOOL — Focus Pocus (tools/focus-pocus/index.qmd)

⟦focuspocus.p1⟧
Writing a PhD thesis is a long exercise in accountability with no one watching. Mine ran to 280 pages, and getting there meant sitting down to write on days when every other tab looked more appealing, the procrastination, the slow drift, the hour that vanishes before you notice. I needed something that *would* watch, not to shame me, but to catch the moment I wandered and pull me back before the hour was gone.

⟦focuspocus.p2⟧
I looked at the focus apps already out there and didn't want them. Too many are built around harvesting what you do, your habits, your schedule, your attention, and selling it on or holding it on a server you don't control. I wasn't willing to trade my privacy for a timer. So I built my own: **Focus Pocus**, a small desktop app that sits in the corner while you work, notices when you have drifted, and nudges you back, and **keeps every scrap of your data on your own machine**.

⟦focuspocus.p3⟧
There are plenty of focus tools built around the Pomodoro idea of fixed work-and-break blocks. Focus Pocus keeps a timer, but the point of this one is *your own accountability*: instead of just counting down, it pays attention to whether you are actually working, and it speaks up when you are not.

⟦focuspocus.nudge⟧
You set an *inactivity threshold*, say ten minutes. If your mouse and keyboard go quiet for longer than that, or if a known time-sink takes over your screen, Focus Pocus pops up and beeps. Ignore it and it does not give up. Each unanswered nudge comes back *louder*, with more beeps than the last, until you deal with it. Gentle at first, hard to tune out by the third.

⟦focuspocus.blocklist.p1⟧
Everyone's rabbit hole is a different shape, so Focus Pocus lets you build your own blocklist. In the settings you add whatever tends to pull you away, one at a time, by the name you would see on its browser tab or in its title bar: `youtube`, `tiktok`, `netflix`, a comfort game, a manga reader. From then on it watches for those words in whatever window is in front of you, and speaks up when one of them lingers too long. Your list is kept in a plain file on your own machine and, like everything else here, never leaves it.

⟦focuspocus.blocklist.p2⟧
A blocklist is a nudge, though, not a locked door. Nothing stops you closing the app, renaming a tab, or talking yourself into a workaround, and Focus Pocus will not wrestle you over it. But if you go hunting for the gap, the only person waiting on the other side is you. This was always meant to be a mirror you hold up to your own focus rather than a cage, so how honestly you use it is, in the end, entirely yours to decide.

⟦focuspocus.privacy.intro⟧
This is the part I care about most. Focus Pocus is not watching your screen, and it never records *what* you were looking at:

⟦focuspocus.privacy.close⟧
You get the accountability without the surveillance. I think everyone deserves that: to be the one in charge of their own data.

⟦focuspocus.afterwards⟧
Each session logs how long you focused, how long you paused, how many times you got nudged, and a self-rating of how the session felt. Over a month that adds up to a picture of when and how you actually work, including the honest gap between how efficient you *felt* and how efficient you *were*.

⟦focuspocus.building.p1⟧
Focus Pocus is a work in progress. Right now it works from two low-level signals: whether your mouse and keyboard have moved, and the title of the window in front of you. I am expanding the list of distraction sites it recognises, cleaning up the session data, and turning these charts into a proper in-app dashboard.

⟦focuspocus.building.p2⟧
Adding your own distractions is now built in. The gap still left is the rare site that gives its name away nowhere, not even in its tab, so there is no word to catch it by; handling those cleanly is the next thing I want to solve.

⟦focuspocus.catch⟧
Focus Pocus is a nudge, not a cure-all. No app can do the hard part for you, at the end of the day the accountability has to be yours. The timer can catch you drifting and call you back, but sitting down and doing the work is still on you. What it gave me was a little more honesty about where my hours actually went, and a louder conscience when I wandered. The thesis still had to be written one page at a time.

---

## TOOL — Reminder Bot (tools/reminder-bot/index.qmd)

⟦reminderbot.intro⟧
Procrastination and ADHD are things my friends and I have always struggled with, and the research says we are not uniquely broken, just part of a very large club: Steel's meta-analysis estimates that 80 to 95 percent of college students procrastinate, and a global review puts symptomatic ADHD at roughly 6.8 percent of adults. What I wanted was accountability I could not dodge, so I moved the nagging into the one place I already have open all day: Discord. **Reminder Bot** is a Discord bot you host yourself that pings you and your friends on your own schedule, **keeps a scoreboard of who followed through**, and keeps every scrap of its data on your own machine.

⟦reminderbot.pings⟧
Give a reminder a time, a title, and the people to tag, and when the moment comes the bot posts it in your channel and pings them. Every reminder can recur on whatever rhythm you want (daily, weekly, or specific weekdays), fire several times a day so ticking any one skips the rest (handy for medication or water), and respect an away schedule so a holiday holds your pings and does not read as a week of failure. Two reactions sit on every reminder: tap ✅ and it counts as done, tap ❌ or ignore it and it counts as a miss. That single tap is the whole scoring system.

⟦reminderbot.reports.p1⟧
The tap-to-complete scoring quietly adds up, and once a week and once a month the bot turns it into a report. Your score is simply the reminders you ticked off divided by the ones you were sent, and each person gets a line of commentary pitched to how they did.

⟦reminderbot.reports.p2⟧
The commentary is the whole personality of the thing. A rough week gets *"The bar was on the floor and you brought a shovel."* There are hundreds of these lines across four tiers, so the roasts and the praise rarely repeat, and the monthly report even crowns a winner. It is silly on purpose, because a scoreboard between friends should be fun to lose as well as to win.

⟦reminderbot.local⟧
Like everything I build, this one keeps to itself. There is no external server and no account: you run it on your own computer with your own bot token, and your reminders, stats, and away schedules all live in plain files next to the bot, yours to read, back up, or wipe.

⟦reminderbot.comingsoon⟧
Reminder Bot works, and it has been running in my own server for months, but it is still wired to my personal bot token and local storage. Once I have generalised the code and tidied it up, I will make it public. For now, consider this a preview of what is coming.
