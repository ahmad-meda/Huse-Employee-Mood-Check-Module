from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import date
from Files.SQLAlchemyModels import MoodCheck, Employee
from sqlalchemy import func

class EmployeeMoodService:
    
    @staticmethod
    def get_mood_check_statistics(db: Session, company_ids: Optional[List[int]] = None, group_id: Optional[int] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict[str, Any]:
        """Get mood statistics with raw values for dashboards and visualization."""
        try:
            # Normalize company_ids to list
            if company_ids is not None and not isinstance(company_ids, list):
                company_ids = [company_ids]
            
            if group_id:
                employees = db.query(Employee).filter(Employee.group_id == group_id, Employee.is_deleted == False).all()
            elif company_ids:
                employees = db.query(Employee).filter(Employee.company_id.in_(company_ids), Employee.is_deleted == False).all()
            else:
                return {"total_records": 0, "message": "No filter criteria provided"}
            
            if not employees:
                return {"total_records": 0, "message": "No employees found"}
            
            employee_ids = [emp.id for emp in employees]
            query = db.query(MoodCheck).filter(MoodCheck.employee_id.in_(employee_ids))
            
            if start_date:
                query = query.filter(MoodCheck.date >= start_date)
            if end_date:
                query = query.filter(MoodCheck.date <= end_date)
            
            records = query.all()
            
            if not records:
                return {"total_records": 0, "message": "No mood data found", "employee_count": len(employee_ids)}
            
            # Aggregate data
            mood_counts = {'1': 0, '2': 0, '3': 0, '4': 0}  # 1=Great, 2=Good, 3=Okay, 4=Not so good
            date_moods = {}
            employee_moods = {}
            mood_values = []
            
            for rec in records:
                mood_counts[rec.mood] = mood_counts.get(rec.mood, 0) + 1
                date_str = rec.date.isoformat() if rec.date else None
                
                if date_str:
                    if date_str not in date_moods:
                        date_moods[date_str] = {'moods': [], 'counts': {'1': 0, '2': 0, '3': 0, '4': 0}}
                    date_moods[date_str]['moods'].append(int(rec.mood))
                    date_moods[date_str]['counts'][rec.mood] += 1
                
                if rec.employee_id not in employee_moods:
                    employee_moods[rec.employee_id] = {'moods': [], 'mood_counts': {'1': 0, '2': 0, '3': 0, '4': 0}}
                employee_moods[rec.employee_id]['moods'].append(int(rec.mood))
                employee_moods[rec.employee_id]['mood_counts'][rec.mood] += 1
                
                try:
                    mood_values.append(int(rec.mood))
                except:
                    pass
            
            if not mood_values:
                return {"total_records": len(records), "message": "No valid mood data"}
            
            import numpy as np
            from scipy import stats as scipy_stats
            
            mood_array = np.array(mood_values)
            
            # Calculate statistics
            mean_mood = float(np.mean(mood_array))
            median_mood = float(np.median(mood_array))
            mode_result = scipy_stats.mode(mood_array, keepdims=True)
            mode_mood = int(mode_result.mode[0])
            std_mood = float(np.std(mood_array, ddof=1))
            variance = float(np.var(mood_array, ddof=1))
            min_mood = int(np.min(mood_array))
            max_mood = int(np.max(mood_array))
            
            # Percentiles
            q1 = float(np.percentile(mood_array, 25))
            q2 = float(np.percentile(mood_array, 50))
            q3 = float(np.percentile(mood_array, 75))
            iqr = q3 - q1
            
            # Distribution percentages (1=Great, 2=Good, 3=Okay, 4=Not so good)
            mood_1_pct = (mood_counts.get('1', 0) / len(records)) * 100  # Great
            mood_2_pct = (mood_counts.get('2', 0) / len(records)) * 100  # Good
            mood_3_pct = (mood_counts.get('3', 0) / len(records)) * 100  # Okay
            mood_4_pct = (mood_counts.get('4', 0) / len(records)) * 100  # Not so good
            
            # Trend calculation (lower mood = better, so negative slope = worsening, positive = improving)
            trend_slope = 0
            trend_direction = "stable"
            daily_averages = {}
            
            if len(date_moods) >= 3:
                sorted_dates = sorted(date_moods.keys())
                daily_avgs = []
                for d in sorted_dates:
                    avg = np.mean(date_moods[d]['moods'])
                    daily_averages[d] = round(float(avg), 2)
                    daily_avgs.append(avg)
                
                if len(daily_avgs) > 1:
                    trend_slope = float(np.polyfit(range(len(daily_avgs)), daily_avgs, 1)[0])
                    # Since higher mood number = worse, positive slope = worsening
                    if trend_slope > 0.05:
                        trend_direction = "worsening"
                    elif trend_slope < -0.05:
                        trend_direction = "improving"
            else:
                for d, data in date_moods.items():
                    daily_averages[d] = round(float(np.mean(data['moods'])), 2)
            
            # Employee-level analysis (higher mood = worse, so at risk if >= 3.0)
            employee_stats = []
            employees_at_risk_ids = []
            
            for emp_id, data in employee_moods.items():
                emp_mean = float(np.mean(data['moods']))
                is_at_risk = emp_mean >= 3.0  # At risk if average is Okay or worse
                employee_stats.append({
                    "employee_id": emp_id,
                    "total_checks": len(data['moods']),
                    "average_mood": round(emp_mean, 2),
                    "mood_counts": data['mood_counts'],
                    "is_at_risk": is_at_risk
                })
                if is_at_risk:
                    employees_at_risk_ids.append(emp_id)
            
            # Skewness and Kurtosis
            skewness = float(scipy_stats.skew(mood_array)) if len(mood_array) >= 3 else None
            kurtosis = float(scipy_stats.kurtosis(mood_array)) if len(mood_array) >= 3 else None
            
            # Outliers
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = mood_array[(mood_array < lower_bound) | (mood_array > upper_bound)]
            outlier_values = [int(x) for x in outliers.tolist()]
            
            # Date range
            date_range_query = db.query(
                func.min(MoodCheck.date).label('earliest'),
                func.max(MoodCheck.date).label('latest')
            ).filter(MoodCheck.employee_id.in_(employee_ids))
            
            if start_date:
                date_range_query = date_range_query.filter(MoodCheck.date >= start_date)
            if end_date:
                date_range_query = date_range_query.filter(MoodCheck.date <= end_date)
            
            date_range_result = date_range_query.first()
            
            # Format date-wise data for dashboard
            date_wise_data = []
            for date_str in sorted(date_moods.keys()):
                data = date_moods[date_str]
                date_wise_data.append({
                    "date": date_str,
                    "average_mood": round(float(np.mean(data['moods'])), 2),
                    "total_responses": len(data['moods']),
                    "mood_counts": data['counts'],
                    "mood_1_pct": round((data['counts']['1'] / len(data['moods'])) * 100, 1),  # Great
                    "mood_2_pct": round((data['counts']['2'] / len(data['moods'])) * 100, 1),  # Good
                    "mood_3_pct": round((data['counts']['3'] / len(data['moods'])) * 100, 1),  # Okay
                    "mood_4_pct": round((data['counts']['4'] / len(data['moods'])) * 100, 1)   # Not so good
                })
            
            return {
                "summary": {
                    "total_records": len(records),
                    "total_employees": len(employee_ids),
                    "employees_participated": len(employee_moods),
                    "employees_not_participated": len(employee_ids) - len(employee_moods),
                    "participation_rate": round((len(employee_moods) / len(employee_ids)) * 100, 2),
                    "date_range": {
                        "start": date_range_result.earliest.isoformat() if date_range_result and date_range_result.earliest else None,
                        "end": date_range_result.latest.isoformat() if date_range_result and date_range_result.latest else None
                    }
                },
                "mood_distribution": {
                    "counts": mood_counts,
                    "percentages": {
                        "mood_1": round(mood_1_pct, 2),  # Great
                        "mood_2": round(mood_2_pct, 2),  # Good
                        "mood_3": round(mood_3_pct, 2),  # Okay
                        "mood_4": round(mood_4_pct, 2)   # Not so good
                    },
                    "labels": {
                        "1": "Great",
                        "2": "Good",
                        "3": "Okay",
                        "4": "Not so good"
                    }
                },
                "statistics": {
                    "mean": round(mean_mood, 2),
                    "median": round(median_mood, 2),
                    "mode": mode_mood,
                    "std_deviation": round(std_mood, 4),
                    "variance": round(variance, 4),
                    "min": min_mood,
                    "max": max_mood,
                    "range": max_mood - min_mood,
                    "quartiles": {
                        "q1": round(q1, 2),
                        "q2": round(q2, 2),
                        "q3": round(q3, 2)
                    },
                    "iqr": round(iqr, 2),
                    "percentiles": {
                        "p10": round(float(np.percentile(mood_array, 10)), 2),
                        "p25": round(q1, 2),
                        "p50": round(q2, 2),
                        "p75": round(q3, 2),
                        "p90": round(float(np.percentile(mood_array, 90)), 2)
                    },
                    "skewness": round(skewness, 4) if skewness is not None else None,
                    "kurtosis": round(kurtosis, 4) if kurtosis is not None else None
                },
                "trend": {
                    "direction": trend_direction,
                    "slope": round(trend_slope, 4),
                    "daily_averages": daily_averages
                },
                "outliers": {
                    "count": len(outlier_values),
                    "values": outlier_values,
                    "bounds": {
                        "lower": round(lower_bound, 2),
                        "upper": round(upper_bound, 2)
                    }
                },
                "date_wise": date_wise_data,
                "employee_wise": employee_stats,
                "risk_analysis": {
                    "employees_at_risk_count": len(employees_at_risk_ids),
                    "employees_at_risk_ids": employees_at_risk_ids,
                    "risk_percentage": round((len(employees_at_risk_ids) / len(employee_moods)) * 100, 2) if len(employee_moods) > 0 else 0
                },
                "filter": {
                    "company_ids": company_ids,
                    "group_id": group_id,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                }
            }
            
        except Exception as e:
            raise Exception(f"Error getting mood statistics: {str(e)}")