from django.db import models


class Job(models.Model):
    WORK_CHOICE = [
        (
            "on-site",
            "On-Site",
        ),
        (
            "hybrid",
            "Hybrid",
        ),
        (
            "remote",
            "Remote",
        ),
    ]

    JOB_TYPE = [
        ("full-time", "Full-Time"),
        ("part-time", "Part-Time"),
        ("contract", "Contract"),
        ("temporary", "Temporary"),
        ("volunteer", "Volunteer"),
        ("intership", "Internship"),
        ("other", "Other"),
    ]
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    job_title = models.CharField(
        max_length=256, help_text="Enter Job title that you are hiring."
    )
    company = models.CharField(max_length=256, help_text="Enter your company name.")
    workplace_type = models.CharField(
        choices=WORK_CHOICE, help_text="Select the work place type."
    )
    location = models.CharField(max_length=200, help_text="Enter work location.")
    job_type = models.CharField(choices=JOB_TYPE, help_text="Select type of job.")
    description = models.TextField(
        help_text="Enter the description of the job such as skills, experience ..etc"
    )
