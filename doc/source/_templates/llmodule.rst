{{ name }}
{{ underline }}

.. automodule:: {{ fullname }}
   :members:

   {% block functions %}
   {% if functions %}
   {% set projmodpair = fullname.split('.') %}
   .. rubric:: {{ 'Functions' if 'build' == name[:5] or
                  projmodpair[-2] == projmodpair[-1] else 'Cells' }}

   .. autosummary::
   {% for item in functions %}
      ~{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   .. rubric:: Classes

   .. autosummary::
   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: Exceptions

   .. autosummary::
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
