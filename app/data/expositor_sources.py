# -*- coding: utf-8 -*-
"""
Deliberately conservative: an expositor only gets a link here if there is
a well-established, stable, freely-accessible archive of their actual
teaching (sermons, commentary, or articles) in English. Where no such
free archive is known to exist (e.g., an author whose works remain under
active commercial copyright with no publisher-sanctioned free archive),
the key is simply omitted — the UI treats that as "no original source
available" rather than guessing at a bookstore or biography link.

Every URL below is a general author/ministry hub, not a guessed
per-chapter deep link — the destination sites have their own search and
navigation to find the specific passage.
"""

SOURCE_MAP = {
    "spurgeon": ("https://www.blueletterbible.org/commentaries/spurgeon_charles/",
                 "Read Spurgeon's sermons at Blue Letter Bible"),
    "macarthur": ("https://www.gty.org/library/sermons-library",
                  "Browse John MacArthur's sermon library at Grace to You"),
    "piper": ("https://www.desiringgod.org/scripture",
              "Browse John Piper's teaching by Scripture at Desiring God"),
    "keller": ("https://gospelinlife.com/sermons/",
               "Browse Tim Keller's sermons at Gospel in Life"),
    "sproul": ("https://www.ligonier.org/learn",
               "Explore R. C. Sproul's teaching at Ligonier Ministries"),
    "henry": ("https://www.blueletterbible.org/commentaries/",
              "Find Matthew Henry's complete commentary at Blue Letter Bible"),
    "wright": ("https://ntwrightpage.com",
               "Explore N. T. Wright's articles and talks"),
    "carson": ("https://www.thegospelcoalition.org/profile/d-a-carson/",
               "Read D. A. Carson's articles at The Gospel Coalition"),
    "smith": ("https://www.blueletterbible.org/audio_video/smith_chuck/",
              "Browse Chuck Smith's verse-by-verse teaching at Blue Letter Bible"),
    "begg": ("https://www.truthforlife.org",
             "Explore Alistair Begg's teaching at Truth For Life"),
    "baucham": ("https://voddiebaucham.org",
                "Explore Voddie Baucham's teaching"),
    "guzik": ("https://enduringword.com/bible-commentary/",
              "Read David Guzik's complete commentary at Enduring Word"),
    "rogers": ("https://www.loveworthfinding.org",
               "Explore Adrian Rogers' sermons at Love Worth Finding"),
    "graham": ("https://billygraham.org/audio_video/classic-sermons/",
               "Browse Billy Graham's classic sermons"),
    "ferguson": ("https://www.ligonier.org/learn",
                 "Explore Sinclair Ferguson's teaching at Ligonier Ministries"),
    "swindoll": ("https://insight.org",
                 "Explore Chuck Swindoll's teaching at Insight for Living"),
    "mcgee": ("https://www.blueletterbible.org/commentaries/mcgee_j_vernon/",
              "Read J. Vernon McGee's Thru the Bible commentary at Blue Letter Bible"),
    # Deliberately omitted (no known stable free full-text/sermon archive):
    # lewis, stott, wiersbe, barclay, tozer, bruce, ryrie, kidner, motyer,
    # davis, kaiser, waltke, sailhamer, duguid.
}
