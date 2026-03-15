{% extends "donor/base.html" %}
{% block content %}
<h2>My Donation History</h2>

<table class="table table-bordered">
    <thead>
        <tr>
            <th>Blood Bank</th>
            <th>Location</th>
            <th>Date</th>
        </tr>
    </thead>
    <tbody>
        {% for d in donations %}
        <tr>
            <td>{{ d.bloodbank.name }}</td>
            <td>{{ d.bloodbank.location }}</td>
            <td>{{ d.date }}</td>
        </tr>
        {% empty %}
        <tr><td colspan="3">No donations yet.</td></tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
