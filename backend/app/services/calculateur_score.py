class CalculateurScore:
    def calculer(self, score_yeux: float, score_levres: float) -> dict:
        score_final = (score_yeux * 0.5) + (score_levres * 0.5)

        if score_final >= 70:
            niveau = "Eleve"
        elif score_final >= 40:
            niveau = "Moyen"
        else:
            niveau = "Faible"

        return {
            "score_yeux": round(score_yeux, 2),
            "score_levres": round(score_levres, 2),
            "score_final": round(score_final, 2),
            "niveau": niveau
        }