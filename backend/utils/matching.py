from typing import Dict, List

from rapidfuzz import fuzz


SKILL_ALIASES: Dict[str, str] = {

    # Frontend
    "reactjs": "react",
    "react.js": "react",
    "nextjs": "next.js",
    "next": "next.js",
    "vuejs": "vue",
    "vue.js": "vue",
    "angularjs": "angular",
    "angular.js": "angular",
    "tailwindcss": "tailwind css",
    "tailwind": "tailwind css",
    "bootstrap5": "bootstrap",
    "bootstrap4": "bootstrap",
    "js": "javascript",
    "ts": "typescript",

    # Backend
    "nodejs": "node.js",
    "node": "node.js",
    "expressjs": "express",
    "express.js": "express",
    "nestjs": "nest.js",
    "dotnet": ".net",
    "asp.net": ".net",
    "aspnet": ".net",
    "springboot": "spring boot",
    "springbootjava": "spring boot",

    # Programming Languages
    "cpp": "c++",
    "c plus plus": "c++",
    "golang": "go",
    "py": "python",

    # Machine Learning / AI
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "genai": "generative ai",
    "llm": "large language models",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "dl": "deep learning",

    # Data Science Libraries
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "tf": "tensorflow",
    "tensor flow": "tensorflow",
    "keras.io": "keras",
    "hf": "hugging face",
    "huggingface": "hugging face",
    "xgboosting": "xgboost",
    "light gbm": "lightgbm",

    # Data Engineering
    "pyspark": "spark",
    "apache spark": "spark",
    "spark sql": "spark",
    "hdfs": "hadoop",
    "apache kafka": "kafka",

    # Databases
    "postgres": "postgresql",
    "postgres sql": "postgresql",
    "postgre": "postgresql",
    "ms sql": "sql server",
    "mssql": "sql server",
    "microsoft sql server": "sql server",
    "mongo": "mongodb",
    "redis cache": "redis",
    "oracle db": "oracle",
    "sqlite3": "sqlite",

    # Cloud
    "amazon web services": "aws",
    "aws cloud": "aws",
    "amazon aws": "aws",
    "google cloud": "gcp",
    "google cloud platform": "gcp",
    "microsoft azure": "azure",
    "azure cloud": "azure",

    # DevOps
    "k8s": "kubernetes",
    "docker container": "docker",
    "docker engine": "docker",
    "jenkins ci": "jenkins",
    "github actions": "github actions",
    "gitlab ci": "gitlab ci/cd",
    "terraform.io": "terraform",
    "ansible automation": "ansible",

    # Operating Systems
    "ubuntu": "linux",
    "centos": "linux",
    "redhat": "linux",
    "rhel": "linux",

    # Version Control
    "github": "git",
    "gitlab": "git",
    "bitbucket": "git",

    # Mobile
    "react native": "react native",
    "rn": "react native",
    "flutter sdk": "flutter",
    "android sdk": "android",
    "ios sdk": "ios",

    # Testing
    "selenium webdriver": "selenium",
    "junit5": "junit",
    "pytest framework": "pytest",
    "cypress.io": "cypress",

    # APIs
    "rest": "rest api",
    "restful api": "rest api",
    "graphql api": "graphql",

    # BI / Analytics
    "power bi": "powerbi",
    "powerbi desktop": "powerbi",
    "tableau desktop": "tableau",

    # Security
    "penetration testing": "pentesting",
    "pen testing": "pentesting",
    "ethical hacking": "pentesting",

    # Big Data
    "apache hadoop": "hadoop",
    "apache hive": "hive",
    "apache flink": "flink",

    # CI/CD
    "continuous integration": "ci/cd",
    "continuous deployment": "ci/cd",

    # Miscellaneous
    "oop": "object oriented programming",
    "oops": "object oriented programming",
    "dsa": "data structures and algorithms",
    "data structures": "data structures and algorithms",
}


def normalize_skill(skill: str) -> str:
    cleaned = skill.strip().lower()
    return SKILL_ALIASES.get(cleaned, cleaned)    # return the value or else return the default value


def fuzzy_match_keywords(
    resume_keywords: List[str],
    jd_keywords: List[str],
    threshold: int = 80,
) -> Dict[str, List[str]]:
    resume_normalized = {normalize_skill(kw): kw for kw in resume_keywords}
    jd_normalized     = {normalize_skill(kw): kw for kw in jd_keywords}

    matched_jd_originals = []
    missing_jd_originals = []

    for jd_canon, jd_original in jd_normalized.items():
        # 1. Exact canonical match
        if jd_canon in resume_normalized:
            matched_jd_originals.append(jd_original)
            continue

        # 2. Fuzzy match against all resume canonical names
        best_score = 0
        for resume_canon in resume_normalized:
            score = fuzz.token_sort_ratio(jd_canon, resume_canon)
            best_score = max(best_score, score)

        if best_score >= threshold:
            matched_jd_originals.append(jd_original)
        else:
            missing_jd_originals.append(jd_original)

    return {
        'matched': sorted(matched_jd_originals),
        'missing': missing_jd_originals,
    }