<!-- Fixed Horizontal Language Switcher Pill Bar (Always: ខ្មែរ | English | Français) -->
<form action="{% url 'set_language' %}" method="post"
      class="inline-flex items-center p-1 rounded-xl bg-slate-100 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700"
      aria-label="Language Switcher">
  {% csrf_token %}
  <input name="next" type="hidden" value="{{ request.get_full_path|slice:'3:' }}" />

  <button type="submit" name="language" value="km"
          class="px-2.5 py-1 rounded-md text-xs font-semibold transition cursor-pointer {% if CURRENT_LANG == 'km' %}bg-[#E61D4E] text-white shadow-sm{% else %}text-slate-600 dark:text-slate-300 hover:text-slate-950 dark:hover:text-white{% endif %}">
    ខ្មែរ
  </button>

  <button type="submit" name="language" value="en"
          class="px-2.5 py-1 rounded-md text-xs font-semibold transition cursor-pointer {% if CURRENT_LANG == 'en' %}bg-[#E61D4E] text-white shadow-sm{% else %}text-slate-600 dark:text-slate-300 hover:text-slate-950 dark:hover:text-white{% endif %}">
    English
  </button>

  <button type="submit" name="language" value="fr"
          class="px-2.5 py-1 rounded-md text-xs font-semibold transition cursor-pointer {% if CURRENT_LANG == 'fr' %}bg-[#E61D4E] text-white shadow-sm{% else %}text-slate-600 dark:text-slate-300 hover:text-slate-950 dark:hover:text-white{% endif %}">
    Français
  </button>
</form>