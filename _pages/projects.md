---
layout: archive
title: "Projects"
permalink: /projects/
author_profile: true
redirect_from:
  - /projects
---

{% include base_path %}

Projects List
======
  <ul>{% for post in site.projects reversed %}
    {% include archive-single.html %}
  {% endfor %}</ul>


