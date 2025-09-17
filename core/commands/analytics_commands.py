"""
Commandes Analytics pour Arkalia Quest
Permet d'accéder aux insights et analytics depuis le terminal
"""

from typing import Any

import requests


class AnalyticsCommands:
    """Commandes pour l'analytics et les insights"""

    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.commands = {
            "analytics": self.cmd_analytics,
            "insights": self.cmd_insights,
            "stats": self.cmd_stats,
            "progress": self.cmd_progress,
            "recommendations": self.cmd_recommendations,
            "learning_style": self.cmd_learning_style,
            "engagement": self.cmd_engagement,
            "export_data": self.cmd_export_data,
        }

    def cmd_analytics(self) -> dict[str, Any]:
        """Affiche les analytics globaux"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics/global", timeout=10)
            if response.status_code == 200:
                data = response.json()
                analytics = data.get("analytics", {})

                message = "📊 ANALYTICS GLOBAUX ARKALIA QUEST\n"
                message += "=" * 50 + "\n\n"

                # Statistiques générales
                message += f"👥 Utilisateurs totaux: {analytics.get('total_users', 0)}\n"
                message += f"🎮 Sessions totales: {analytics.get('total_sessions', 0)}\n"
                message += f"⏱️ Temps de jeu total: {analytics.get('total_playtime_hours', 0)}h\n"
                message += f"📊 Temps moyen par utilisateur: {analytics.get('avg_playtime_per_user', 0)}h\n\n"

                # Sessions récentes
                message += f"📈 Sessions (7 derniers jours): {analytics.get('recent_sessions_7_days', 0)}\n\n"

                # Métriques d'engagement
                engagement = analytics.get("engagement_metrics", {})
                if engagement:
                    message += "📊 MÉTRIQUES D'ENGAGEMENT:\n"
                    message += f"🔄 Taux de rétention (7j): {engagement.get('retention_rate_7_days', 0)}%\n"
                    message += f"✅ Taux de complétion missions: {engagement.get('mission_completion_rate', 0)}%\n"
                    message += f"⭐ Score d'engagement moyen: {engagement.get('avg_engagement_score', 0)}/100\n\n"

                # Événements populaires
                popular_events = analytics.get("popular_events", {})
                if popular_events:
                    message += "🔥 ÉVÉNEMENTS POPULAIRES:\n"
                    for event, count in list(popular_events.items())[:5]:
                        event_name = self._format_event_name(event)
                        message += f"• {event_name}: {count}\n"

                return {
                    "réussite": True,
                    "ascii_art": "📊",
                    "message": message,
                    "score_gagne": 5,
                    "profile_updated": False,
                }
            else:
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": "❌ Erreur lors de la récupération des analytics",
                    "score_gagne": 0,
                    "profile_updated": False,
                }
        except Exception as e:
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur: {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def cmd_insights(self) -> dict[str, Any]:
        """Affiche les insights personnalisés"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics/insights", timeout=10)
            if response.status_code == 200:
                data = response.json()
                insights = data.get("insights", {})

                if not insights:
                    return {
                        "réussite": False,
                        "ascii_art": "❌",
                        "message": "❌ Aucun insight disponible pour le moment",
                        "score_gagne": 0,
                        "profile_updated": False,
                    }

                message = "📊 VOS INSIGHTS PERSONNALISÉS\n"
                message += "=" * 50 + "\n\n"

                # Statistiques générales
                message += f"🎮 Sessions totales: {insights.get('total_sessions', 0)}\n"
                message += f"⏱️ Temps de jeu total: {insights.get('total_playtime_hours', 0)}h\n"
                message += f"📈 Taux d'engagement: {insights.get('engagement_rate', 0)}%\n"
                message += f"🏆 Niveau actuel: {insights.get('current_level', 1)}\n\n"

                # Missions et jeux
                message += f"🎯 Missions complétées: {insights.get('missions_completed', 0)}\n"
                message += f"🎲 Jeux complétés: {insights.get('games_completed', 0)}\n"
                message += f"🏅 Badges gagnés: {insights.get('badges_earned', 0)}\n\n"

                # Style d'apprentissage
                learning_style = insights.get("learning_style", "unknown")
                message += (
                    f"🧠 Style d'apprentissage: {self._format_learning_style(learning_style)}\n\n"
                )

                # Jeux préférés
                preferred_games = insights.get("preferred_games", [])
                if preferred_games:
                    message += f"🎮 Jeux préférés: {', '.join(preferred_games)}\n\n"

                # Dernière activité
                last_active = insights.get("last_active_days", 0)
                message += f"🕐 Dernière activité: il y a {last_active} jours\n\n"

                # Recommandations
                recommendations = insights.get("recommendations", [])
                if recommendations:
                    message += "💡 RECOMMANDATIONS PERSONNALISÉES:\n"
                    for i, rec in enumerate(recommendations, 1):
                        message += f"{i}. {rec}\n"

                return {
                    "réussite": True,
                    "ascii_art": "🔍",
                    "message": message,
                    "score_gagne": 10,
                    "profile_updated": False,
                }
            else:
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": "❌ Erreur lors de la récupération des insights",
                    "score_gagne": 0,
                    "profile_updated": False,
                }
        except Exception as e:
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur: {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def cmd_stats(self) -> dict[str, Any]:
        """Affiche les statistiques détaillées"""
        try:
            # Récupérer les insights
            response = requests.get(f"{self.base_url}/api/analytics/insights", timeout=10)
            if response.status_code == 200:
                data = response.json()
                insights = data.get("insights", {})

                message = "📈 STATISTIQUES DÉTAILLÉES\n"
                message += "=" * 50 + "\n\n"

                # Statistiques de progression
                message += "🎯 PROGRESSION:\n"
                message += f"• Niveau: {insights.get('current_level', 1)}\n"
                message += f"• Missions complétées: {insights.get('missions_completed', 0)}\n"
                message += f"• Jeux complétés: {insights.get('games_completed', 0)}\n"
                message += f"• Badges gagnés: {insights.get('badges_earned', 0)}\n\n"

                # Statistiques de temps
                message += "⏱️ TEMPS DE JEU:\n"
                message += f"• Total: {insights.get('total_playtime_hours', 0)}h\n"
                message += f"• Sessions: {insights.get('total_sessions', 0)}\n"
                message += f"• Moyenne par session: {insights.get('avg_session_duration_minutes', 0)}min\n\n"

                # Statistiques d'engagement
                message += "📊 ENGAGEMENT:\n"
                message += f"• Taux d'engagement: {insights.get('engagement_rate', 0)}%\n"
                message += f"• Dernière activité: {insights.get('last_active_days', 0)} jours\n\n"

                # Statistiques de profil
                message += "👤 PROFIL:\n"
                message += f"• Style d'apprentissage: {self._format_learning_style(insights.get('learning_style', 'unknown'))}\n"

                preferred_games = insights.get("preferred_games", [])
                if preferred_games:
                    message += f"• Jeux préférés: {', '.join(preferred_games)}\n"

                return {
                    "réussite": True,
                    "ascii_art": "📊",
                    "message": message,
                    "score_gagne": 8,
                    "profile_updated": False,
                }
            else:
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": "❌ Erreur lors de la récupération des statistiques",
                    "score_gagne": 0,
                    "profile_updated": False,
                }
        except Exception as e:
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur: {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def cmd_progress(self) -> dict[str, Any]:
        """Affiche la progression détaillée"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics/insights", timeout=10)
            if response.status_code == 200:
                data = response.json()
                insights = data.get("insights", {})

                message = "🎯 PROGRESSION DÉTAILLÉE\n"
                message += "=" * 50 + "\n\n"

                # Progression générale
                level = insights.get("current_level", 1)
                missions = insights.get("missions_completed", 0)
                games = insights.get("games_completed", 0)
                badges = insights.get("badges_earned", 0)

                message += f"🏆 NIVEAU ACTUEL: {level}\n"
                message += "📊 PROGRESSION GLOBALE:\n"
                message += f"• Missions: {missions} complétées\n"
                message += f"• Jeux: {games} complétés\n"
                message += f"• Badges: {badges} gagnés\n\n"

                # Calculer les pourcentages (estimations)
                mission_progress = min((missions / 50) * 100, 100)  # 50 missions estimées
                game_progress = min((games / 20) * 100, 100)  # 20 jeux estimés
                badge_progress = min((badges / 30) * 100, 100)  # 30 badges estimés

                message += "📈 POURCENTAGES DE PROGRESSION:\n"
                message += f"• Missions: {mission_progress:.1f}%\n"
                message += f"• Jeux: {game_progress:.1f}%\n"
                message += f"• Badges: {badge_progress:.1f}%\n\n"

                # Recommandations de progression
                message += "💡 CONSEILS POUR PROGRESSER:\n"
                if mission_progress < 50:
                    message += "• Complète plus de missions pour monter en niveau\n"
                if game_progress < 50:
                    message += "• Essaie différents types de jeux éducatifs\n"
                if badge_progress < 50:
                    message += "• Débloque de nouveaux badges en explorant\n"
                if mission_progress >= 80 and game_progress >= 80:
                    message += (
                        "• Excellent travail ! Continue d'explorer les fonctionnalités avancées\n"
                    )

                return {
                    "réussite": True,
                    "ascii_art": "🎯",
                    "message": message,
                    "score_gagne": 7,
                    "profile_updated": False,
                }
            else:
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": "❌ Erreur lors de la récupération de la progression",
                    "score_gagne": 0,
                    "profile_updated": False,
                }
        except Exception as e:
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur: {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def cmd_recommendations(self) -> dict[str, Any]:
        """Affiche les recommandations personnalisées"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics/insights", timeout=10)
            if response.status_code == 200:
                data = response.json()
                insights = data.get("insights", {})
                recommendations = insights.get("recommendations", [])

                if not recommendations:
                    return {
                        "réussite": False,
                        "ascii_art": "❌",
                        "message": "❌ Aucune recommandation disponible pour le moment",
                        "score_gagne": 0,
                        "profile_updated": False,
                    }

                message = "💡 RECOMMANDATIONS PERSONNALISÉES\n"
                message += "=" * 50 + "\n\n"

                for i, rec in enumerate(recommendations, 1):
                    message += f"{i}. {rec}\n"

                message += "\n🎯 Ces recommandations sont basées sur:\n"
                message += f"• Votre style d'apprentissage: {self._format_learning_style(insights.get('learning_style', 'unknown'))}\n"
                message += f"• Votre niveau actuel: {insights.get('current_level', 1)}\n"
                message += f"• Votre taux d'engagement: {insights.get('engagement_rate', 0)}%\n"

                return {
                    "réussite": True,
                    "ascii_art": "💡",
                    "message": message,
                    "score_gagne": 6,
                    "profile_updated": False,
                }
            else:
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": "❌ Erreur lors de la récupération des recommandations",
                    "score_gagne": 0,
                    "profile_updated": False,
                }
        except Exception as e:
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur: {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def cmd_learning_style(self) -> dict[str, Any]:
        """Affiche l'analyse du style d'apprentissage"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics/insights", timeout=10)
            if response.status_code == 200:
                data = response.json()
                insights = data.get("insights", {})
                learning_style = insights.get("learning_style", "unknown")

                message = "🧠 ANALYSE DU STYLE D'APPRENTISSAGE\n"
                message += "=" * 50 + "\n\n"

                message += f"🎯 VOTRE STYLE: {self._format_learning_style(learning_style)}\n\n"

                # Description détaillée du style
                style_descriptions = {
                    "guided_learner": "Vous préférez suivre des tutoriels étape par étape et avoir des "
                    "instructions claires. Vous aimez apprendre de manière structurée et progressive.",
                    "hands_on_learner": "Vous apprenez mieux en expérimentant directement. "
                    "Vous préférez essayer par vous-même et découvrir les solutions de manière pratique.",
                    "support_seeker": "Vous n'hésitez pas à demander de l'aide quand vous en avez besoin. "
                    "Vous utilisez les indices et le support pour progresser efficacement.",
                    "balanced_learner": "Vous adaptez votre approche selon les situations. "
                    "Vous combinez différentes méthodes d'apprentissage pour optimiser vos résultats.",
                    "unknown": "Votre style d'apprentissage n'a pas encore été déterminé. "
                    "Continuez à jouer pour que nous puissions l'analyser.",
                }

                message += f"📝 DESCRIPTION:\n{style_descriptions.get(learning_style, 'Style non reconnu')}\n\n"

                # Conseils personnalisés
                message += "💡 CONSEILS PERSONNALISÉS:\n"
                if learning_style == "guided_learner":
                    message += "• Suivez les tutoriels dans l'ordre\n"
                    message += "• Lisez attentivement les instructions\n"
                    message += "• Prenez le temps de comprendre chaque étape\n"
                elif learning_style == "hands_on_learner":
                    message += "• Expérimentez avec les commandes\n"
                    message += "• Essayez différentes approches\n"
                    message += "• N'hésitez pas à faire des erreurs pour apprendre\n"
                elif learning_style == "support_seeker":
                    message += "• Utilisez les indices quand vous êtes bloqué\n"
                    message += "• Demandez de l'aide via le chat\n"
                    message += "• Consultez la documentation\n"
                elif learning_style == "balanced_learner":
                    message += "• Adaptez votre approche selon les défis\n"
                    message += "• Combinez tutoriels et expérimentation\n"
                    message += "• Variez vos méthodes d'apprentissage\n"

                return {
                    "réussite": True,
                    "ascii_art": "🧠",
                    "message": message,
                    "score_gagne": 9,
                    "profile_updated": False,
                }
            else:
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": "❌ Erreur lors de l'analyse du style d'apprentissage",
                    "score_gagne": 0,
                    "profile_updated": False,
                }
        except Exception as e:
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur: {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def cmd_engagement(self) -> dict[str, Any]:
        """Affiche les métriques d'engagement"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics/insights", timeout=10)
            if response.status_code == 200:
                data = response.json()
                insights = data.get("insights", {})

                message = "📊 MÉTRIQUES D'ENGAGEMENT\n"
                message += "=" * 50 + "\n\n"

                engagement_rate = insights.get("engagement_rate", 0)
                last_active = insights.get("last_active_days", 0)
                total_sessions = insights.get("total_sessions", 0)
                avg_session_duration = insights.get("avg_session_duration_minutes", 0)

                message += f"⭐ SCORE D'ENGAGEMENT: {engagement_rate}%\n\n"

                # Interprétation du score
                if engagement_rate >= 80:
                    message += "🎉 Excellent engagement ! Vous êtes très actif.\n"
                elif engagement_rate >= 60:
                    message += "👍 Bon engagement ! Vous participez régulièrement.\n"
                elif engagement_rate >= 40:
                    message += "📈 Engagement moyen. Il y a de la place pour s'améliorer.\n"
                else:
                    message += "📉 Engagement faible. Essayez de jouer plus régulièrement.\n"

                message += "\n📈 DÉTAILS:\n"
                message += f"• Sessions totales: {total_sessions}\n"
                message += f"• Durée moyenne par session: {avg_session_duration}min\n"
                message += f"• Dernière activité: il y a {last_active} jours\n\n"

                # Conseils d'amélioration
                message += "💡 CONSEILS POUR AMÉLIORER L'ENGAGEMENT:\n"
                if engagement_rate < 60:
                    message += "• Jouez plus régulièrement\n"
                    message += "• Explorez de nouvelles fonctionnalités\n"
                    message += "• Participez aux défis communautaires\n"
                    message += "• Débloquez de nouveaux badges\n"
                else:
                    message += "• Continuez votre excellent travail !\n"
                    message += "• Essayez les fonctionnalités avancées\n"
                    message += "• Aidez les autres joueurs\n"

                return {
                    "réussite": True,
                    "ascii_art": "📊",
                    "message": message,
                    "score_gagne": 8,
                    "profile_updated": False,
                }
            else:
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": "❌ Erreur lors de la récupération des métriques d'engagement",
                    "score_gagne": 0,
                    "profile_updated": False,
                }
        except Exception as e:
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur: {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def cmd_export_data(self) -> dict[str, Any]:
        """Exporte les données analytics"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics/export", timeout=10)
            if response.status_code == 200:
                # data = response.json()  # Variable non utilisée

                message = "📤 EXPORT DES DONNÉES ANALYTICS\n"
                message += "=" * 50 + "\n\n"

                message += "✅ Export réussi !\n\n"
                message += "📊 Données exportées:\n"
                message += "• Vos insights personnalisés\n"
                message += "• Votre historique d'activité\n"
                message += "• Vos statistiques de progression\n"
                message += "• Vos métriques d'engagement\n\n"

                message += "🔒 Vos données sont anonymisées et sécurisées.\n"
                message += "📝 Format: JSON\n"

                return {
                    "réussite": True,
                    "ascii_art": "📤",
                    "message": message,
                    "score_gagne": 5,
                    "profile_updated": False,
                }
            else:
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": "❌ Erreur lors de l'export des données",
                    "score_gagne": 0,
                    "profile_updated": False,
                }
        except Exception as e:
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur: {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def _format_learning_style(self, style: str) -> str:
        """Formate le style d'apprentissage pour l'affichage"""
        styles = {
            "guided_learner": "Apprenant guidé (préfère les tutoriels)",
            "hands_on_learner": "Apprenant pratique (préfère l'expérimentation)",
            "support_seeker": "Demandeur d'aide (utilise indices et support)",
            "balanced_learner": "Apprenant équilibré",
            "unknown": "Non déterminé",
        }
        return styles.get(style, style)

    def _format_event_name(self, event: str) -> str:
        """Formate le nom d'un événement pour l'affichage"""
        names = {
            "command_executed": "Commandes exécutées",
            "mission_start": "Missions démarrées",
            "mission_complete": "Missions complétées",
            "game_start": "Jeux démarrés",
            "game_complete": "Jeux complétés",
            "tutorial_start": "Tutoriels démarrés",
            "badge_earned": "Badges gagnés",
            "session_start": "Sessions démarrées",
        }
        return names.get(event, event)
