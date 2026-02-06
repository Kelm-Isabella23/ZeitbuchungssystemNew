from django import forms  # Stellt Django-Formulare und ModelForm-Funktionalität bereit: wirdrd verwendet, um Benutzereingaben zu erfassen und zu validieren
from time_tracker.models import Module, Report  #Importiert die relevanten Datenmodelle, auf denen das Formular basiert


class ReportForm(forms.ModelForm):
    """
    Formular zur Erfassung und Bearbeitung von Zeitbuchungen (basierend auf dem Report-Modell mit zusätzlicher Validierungs- und Anzeige-Logik)
    """

    class Meta:
    
        model = Report #Verknüpft das Formular mit dem Report-Datenmodell

        fields = ["date", "minutes", "module", "text"]

        # Passt die Darstellung einzelner Felder an:
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "minutes": forms.NumberInput(attrs={"min": 1}),
            "text": forms.TextInput(
                attrs={"maxlength": 300, "style": "width: 420px;"}
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialisiert das Formular (Filtert auswählbare Module und passt Feldbezeichnungen für die Benutzeroberfläche an)
        """
        super().__init__(*args, **kwargs)

        active = Module.objects.filter(is_active=True).order_by("name") #nur aktive Module für die Auswahl

        #Beim Bearbeiten eines bestehenden Reports
        if self.instance and self.instance.pk and self.instance.module_id:
            active = active | Module.objects.filter(pk=self.instance.module_id)

        #setzt die gefilterte Modulauswahl im Formular
        self.fields["module"].queryset = active.distinct()

        self.fields["date"].label = "Datum"
        self.fields["minutes"].label = "Minuten"
        self.fields["module"].label = "Modul"
        self.fields["text"].label = "Kurzbericht"

    def clean_minutes(self):
        """
        Validiert die eingegebene Minutenanzahl
        """
        minutes = self.cleaned_data["minutes"]

        if minutes <= 0:
            raise forms.ValidationError(
                "Minuten müssen eine positive Zahl sein."
            )

        return minutes

    def clean_text(self):
        """
        Validiert den Kurzbericht (entfernt Leerzeichen und begrenzt die Länge)
        """
        text = (self.cleaned_data.get("text") or "").strip()

        if not text:
            raise forms.ValidationError(
                "Bitte Kurzbericht ausfüllen."
            )

        #Sicherheitsbegrenzung der Textlänge
        return text[:300]
