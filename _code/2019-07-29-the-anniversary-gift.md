---
layout: post
title: 'The anniversary gift'
date: 2019-07-29 22:54:34
categories: code
tags: code
---

Sometimes you feel like you have to do something good for someone you love. Build something for them. Or save them some money. Make their life easier in some way. That is how I felt one weekend when I decided to set up a blog for my partner. She had been thinking of a way to present some of her creative work on the cheap. She had the need, I was learning how to play with docker and thought I could have some fun.

Setting up a Wordpress instance was not too much of a hassle, so before she knew it she was the proud owner of a domain name pointing to a Wordpress instance running on AWS. We transferred some content from a previous blog and started adding more to the current one. We experimented with a few themes and had good fun. It all went well for years...

And then one day, on our anniversary, she asked me to help her "hack" into her blog. I thought she just forgot her password and I just need to "find" it for her or check if I have a back up somewhere. It turned out that she didn't remember her password a few days prior and decided to change it. Then she didn't make note of it and forgot it. None of the passwords we tried worked.

I thought: hey I'll just ssh onto the node and restore the password from the database. Little did I know of what was to come.

First, I needed to find the AWS credentials that I made for her. That was a while back and I hadn't switched to a password manager so that took some digging but it wasn't too bad. What hit me by surprise was the PEM file. I had completely forgotten about it. I didn't have a copy on any of my machines or servers or inboxes or backup drives or cloud storage accounts.

Panic ensued. AWS does not allow you to change your PEM once you've run the instance. If I can't recover the PEM, I can't recover the node and all the content on it. The bast I can do is scrape it.

In a moment of desperation, I checked a very old place I kept secret stuff. One of those "security through obscurity" places that I should have gotten rid of a long time ago. The key was there, stored in a slightly convoluted way but there.

Updating the password took some effort in remembering but was pretty much as straightforward as I thought it would be. This time I created a user for myself. Just in case.

There are some lessons in this boring story:

1. Use a password manager!
2. Use a password manager for more than just passwords!
3. If you are setting something up, write a readme file. Just notes on what's where and how to get it. It will help so much!
