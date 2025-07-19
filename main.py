package com.example.quizapp;

import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class MainActivity extends AppCompatActivity {

    TextView tvQuestion, tvStatus;
    Button btnHint, btnSave, btnQuit;
    Button[] optionButtons = new Button[4];

    class Question {
        String q;
        List<String> options;
        String answer;
        Question(String q, List<String> options, String answer) {
            this.q = q;
            this.options = options;
            this.answer = answer;
        }
    }

    List<Question> questions = new ArrayList<>();
    List<Integer> questionsOrder;
    int currentQIndex = 0;
    int attemptsLeft = 3;
    int hintsLeft = 3;
    int score = 0;

    final int attemptsPerQuestion = 3;
    final int totalHints = 3;

    SharedPreferences prefs;
    Random random = new Random();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvQuestion = findViewById(R.id.tvQuestion);
        tvStatus = findViewById(R.id.tvStatus);
        btnHint = findViewById(R.id.btnHint);
        btnSave = findViewById(R.id.btnSave);
        btnQuit = findViewById(R.id.btnQuit);

        optionButtons[0] = findViewById(R.id.btnOption1);
        optionButtons[1] = findViewById(R.id.btnOption2);
        optionButtons[2] = findViewById(R.id.btnOption3);
        optionButtons[3] = findViewById(R.id.btnOption4);

        prefs = getSharedPreferences("quiz_save", Context.MODE_PRIVATE);

        loadQuestions();
        loadProgress();
        setListeners();
        showQuestion();
    }

    void loadQuestions() {
        questions.add(new Question("ما هو أول سورة في القرآن الكريم؟", Arrays.asList("الفاتحة", "البقرة", "آل عمران", "الأنفال"), "الفاتحة"));
        questions.add(new Question("من هو نبي الإسلام؟", Arrays.asList("موسى", "عيسى", "محمد", "إبراهيم"), "محمد"));
        questions.add(new Question("كم عدد أركان الإسلام؟", Arrays.asList("3", "5", "7", "10"), "5"));
        questions.add(new Question("ما هي عاصمة المملكة العربية السعودية؟", Arrays.asList("الرياض", "جدة", "مكة", "الدمام"), "الرياض"));
        questions.add(new Question("ما هو أطول نهر في العالم؟", Arrays.asList("النيل", "الأمازون", "الدا نوب", "الميسيسيبي"), "النيل"));
        questions.add(new Question("من هو الصحابي الذي لقب بـ الفاروق؟", Arrays.asList("عمر بن الخطاب", "أبو بكر الصديق", "علي بن أبي طالب", "عثمان بن عفان"), "عمر بن الخطاب"));
        questions.add(new Question("ما اسم جبل النبي موسى عليه السلام؟", Arrays.asList("الطور", "الحراء", "الكعبة", "أحد"), "الطور"));
        questions.add(new Question("ما هي أكبر قارة في العالم؟", Arrays.asList("آسيا", "أفريقيا", "أوروبا", "أمريكا الشمالية"), "آسيا"));
        questions.add(new Question("ما هو الحيوان الذي يرمز إليه بأنه ملك الغابة؟", Arrays.asList("الأسد", "النمر", "الفيل", "الدب"), "الأسد"));
        questions.add(new Question("كم عدد أيام الأسبوع؟", Arrays.asList("5", "6", "7", "8"), "7"));
        questions.add(new Question("ما هو اسم البحر الذي يقع بين السعودية ومصر؟", Arrays.asList("البحر الأحمر", "البحر الأبيض المتوسط", "خليج العقبة", "البحر الأسود"), "البحر الأحمر"));
        questions.add(new Question("ما هي عاصمة الأردن؟", Arrays.asList("عمان", "دمشق", "بيروت", "القدس"), "عمان"));
        questions.add(new Question("من هو مؤسس علم الجبر؟", Arrays.asList("الخوارزمي", "ابن سينا", "الرازي", "الفرابي"), "الخوارزمي"));
        questions.add(new Question("كم عدد ركعات صلاة الفجر؟", Arrays.asList("2", "4", "3", "5"), "2"));
        questions.add(new Question("أي من هذه البلدان ليست عربية؟", Arrays.asList("تركيا", "مصر", "العراق", "سوريا"), "تركيا"));
        questions.add(new Question("ما هو اسم الكتاب المقدس في المسيحية؟", Arrays.asList("الإنجيل", "القرآن", "التوراة", "الزبور"), "الإنجيل"));
        questions.add(new Question("في أي قارة تقع دولة المغرب؟", Arrays.asList("أفريقيا", "آسيا", "أوروبا", "أمريكا"), "أفريقيا"));
        questions.add(new Question("ما هو الحيوان الذي لا ينام؟", Arrays.asList("الفهد", "الدلفين", "التمساح", "الحصان"), "الدلفين"));
        questions.add(new Question("ما هو اسم عاصمة فرنسا؟", Arrays.asList("باريس", "روما", "مدريد", "برلين"), "باريس"));
        questions.add(new Question("من هو الخليفة الراشد الأول؟", Arrays.asList("أبو بكر الصديق", "عمر بن الخطاب", "عثمان بن عفان", "علي بن أبي طالب"), "أبو بكر الصديق"));
        questions.add(new Question("كم عدد سور القرآن الكريم؟", Arrays.asList("114", "99", "120", "150"), "114"));
        questions.add(new Question("ما اسم مدينة الرسول صلى الله عليه وسلم؟", Arrays.asList("المدينة المنورة", "مكة المكرمة", "الرباط", "دمشق"), "المدينة المنورة"));
        questions.add(new Question("ما هو أسرع حيوان بري؟", Arrays.asList("الفهد", "الأسد", "الغزال", "الكنغر"), "الفهد"));
        questions.add(new Question("أي من هذه الدول تقع في قارة آسيا؟", Arrays.asList("اليابان", "البرتغال", "البرازيل", "المكسيك"), "اليابان"));
        questions.add(new Question("كم عدد ركعات صلاة العشاء؟", Arrays.asList("4", "3", "2", "5"), "4"));
        questions.add(new Question("ما هو اسم أطول برج في العالم؟", Arrays.asList("برج خليفة", "برج إيفل", "برج بيزا", "برج العرب"), "برج خليفة"));
        questions.add(new Question("من هو مؤلف ألف ليلة وليلة؟", Arrays.asList("غير معروف", "نجيب محفوظ", "طه حسين", "جبران خليل جبران"), "غير معروف"));
        questions.add(new Question("ما هو اسم أصغر دولة في العالم؟", Arrays.asList("الفاتيكان", "مونتينيغرو", "ليختنشتاين", "سان مارينو"), "الفاتيكان"));
        questions.add(new Question("في أي سنة هاجر النبي محمد صلى الله عليه وسلم إلى المدينة؟", Arrays.asList("622 ميلادية", "610 ميلادية", "632 ميلادية", "600 ميلادية"), "622 ميلادية"));
        questions.add(new Question("ما هو اسم أطول نهر في أمريكا الجنوبية؟", Arrays.asList("الأمازون", "النيـل", "الميسيسيبي", "اليانغتسي"), "الأمازون"));
        questions.add(new Question("ما هي عاصمة مصر؟", Arrays.asList("القاهرة", "الإسكندرية", "الجيزة", "أسوان"), "القاهرة"));
        questions.add(new Question("من هو أول من آمن من الرجال في الإسلام؟", Arrays.asList("أبو بكر الصديق", "عمر بن الخطاب", "عثمان بن عفان", "علي بن أبي طالب"), "أبو بكر الصديق"));
        questions.add(new Question("ما هو الحيوان الذي يطلق عليه لقب سفينة الصحراء؟", Arrays.asList("الجمل", "الحصان", "الزرافة", "الحمامة"), "الجمل"));
        questions.add(new Question("ما هو اسم أطول جدار في العالم؟", Arrays.asList("سور الصين العظيم", "سور برلين", "سور القدس", "سور بغداد"), "سور الصين العظيم"));
        questions.add(new Question("ما اسم القارة التي تضم مصر والسودان وليبيا؟", Arrays.asList("أفريقيا", "آسيا", "أوروبا", "أمريكا"), "أفريقيا"));
        questions.add(new Question("ما هو اسم الكعبة المشرفة؟", Arrays.asList("بيت الله الحرام", "بيت النبي", "بيت القدس", "بيت السلام"), "بيت الله الحرام"));
        questions.add(new Question("كم عدد سور المفصل في القرآن؟", Arrays.asList("37", "20", "114", "10"), "37"));
        questions.add(new Question("أي دولة تعرف بأنها بلاد الأهرامات؟", Arrays.asList("مصر", "العراق", "تركيا", "لبنان"), "مصر"));
        questions.add(new Question("ما اسم الصلاة التي تؤدى بعد صلاة العصر؟", Arrays.asList("صلاة الضحى", "صلاة الفجر", "صلاة التراويح", "صلاة العشاء"), "صلاة الضحى"));
        questions.add(new Question("ما هو اسم النبي الذي ابتلعه الحوت؟", Arrays.asList("يونس", "نوح", "موسى", "عيسى"), "يونس"));
        questions.add(new Question("ما هو اسم البحر الذي يحيط بجزر المالديف؟", Arrays.asList("المحيط الهندي", "البحر الأحمر", "البحر الأبيض المتوسط", "البحر الكاريبي"), "المحيط الهندي"));
        questions.add(new Question("من هو مؤلف كتاب المبادئ في الفلسفة؟", Arrays.asList("ابن رشد", "ابن سينا", "الفارابي", "الغزالي"), "ابن رشد"));
        questions.add(new Question("ما هو اسم أصغر عظمة في جسم الإنسان؟", Arrays.asList("ركاب الأذن", "الظفر", "الوتر", "القصبة الهوائية"), "ركاب الأذن"));
        questions.add(new Question("ما هي أكبر مدينة في العالم من حيث عدد السكان؟", Arrays.asList("طوكيو", "دلهي", "شنغهاي", "مومباي"), "طوكيو"));
        questions.add(new Question("ما هو اسم السورة التي تسمى قلب القرآن؟", Arrays.asList("يس", "الرحمن", "الملك", "الفاتحة"), "يس"));
        questions.add(new Question("كم عدد الركعات في صلاة الظهر؟", Arrays.asList("4", "2", "3", "5"), "4"));
        questions.add(new Question("ما اسم الملك الذي بنى مدينة البتراء؟", Arrays.asList("البترائيون", "النبطيون", "الحضرميون", "الأنباط"), "الأنباط"));
        questions.add(new Question("ما هو اسم المسجد الذي بناه النبي محمد في المدينة؟", Arrays.asList("المسجد النبوي", "المسجد الحرام", "المسجد الأقصى", "المسجد الأزهري"), "المسجد النبوي"));
        questions.add(new Question("ما هي عاصمة تركيا؟", Arrays.asList("أنقرة", "اسطنبول", "إزمير", "بورصة"), "أنقرة"));
        questions.add(new Question("ما هو اسم أول خليفة في الإسلام؟", Arrays.asList("أبو بكر الصديق", "عمر بن الخطاب", "عثمان بن عفان", "علي بن أبي طالب"), "أبو بكر الصديق"));
        questions.add(new Question("كم عدد أبواب الجنة؟", Arrays.asList("8", "7", "6", "5"), "8"));
        questions.add(new Question("من هو مؤلف كتاب ألف ليلة وليلة؟", Arrays.asList("غير معروف", "جبران خليل جبران", "نجيب محفوظ", "طه حسين"), "غير معروف"));
        questions.add(new Question("ما هو اسم النهر الذي يمر عبر مدينة بغداد؟", Arrays.asList("دجلة", "الفرات", "النيل", "الأمازون"), "دجلة"));
        questions.add(new Question("ما هو الحيوان الذي يعرف بملك الزواحف؟", Arrays.asList("التمساح", "الثعبان", "السلحفاة", "الوزغة"), "التمساح"));
        questions.add(new Question("ما هو اسم المسجد الذي يقع في مكة؟", Arrays.asList("المسجد الحرام", "المسجد النبوي", "المسجد الأقصى", "مسجد قبة الصخرة"), "المسجد الحرام"));
        questions.add(new Question("ما اسم أول كتاب في التاريخ؟", Arrays.asList("كتاب الموتى", "القرآن الكريم", "الأوديسة", "الإنجيل"), "كتاب الموتى"));
        questions.add(new Question("ما هو الحيوان الذي يقال عنه (سفينة الصحراء)؟", Arrays.asList("الجمل", "الماعز", "الحصان", "النعامة"), "الجمل"));
        questions.add(new Question("ما اسم العاصمة الفرنسية؟", Arrays.asList("باريس", "ليون", "مارسيليا", "نيس"), "باريس"));
        questions.add(new Question("كم عدد ساعات اليوم؟", Arrays.asList("24", "12", "36", "48"), "24"));
        questions.add(new Question("ما اسم أقرب كوكب إلى الشمس؟", Arrays.asList("عطارد", "الزهرة", "الأرض", "المريخ"), "عطارد"));
        questions.add(new Question("ما هي العملة الرسمية في اليابان؟", Arrays.asList("الين", "الدولار", "اليورو", "الريال"), "الين"));
        questions.add(new Question("ما اسم البحر الذي يفصل بين السعودية ومصر؟", Arrays.asList("البحر الأحمر", "البحر الأبيض المتوسط", "البحر الكاريبي", "البحر الأسود"), "البحر الأحمر"));
        questions.add(new Question("كم عدد أسابيع السنة؟", Arrays.asList("52", "48", "60", "40"), "52"));
        questions.add(new Question("ما هو اسم أكبر محيط في العالم؟", Arrays.asList("المحيط الهادئ", "المحيط الأطلسي", "المحيط الهندي", "المحيط المتجمد الشمالي"), "المحيط الهادئ"));
        questions.add(new Question("ما اسم الفاكهة التي تسمى ملكة الفواكه؟", Arrays.asList("المانجو", "التفاح", "الموز", "الأناناس"), "المانجو"));
        questions.add(new Question("ما هو الحيوان الذي له خرطوم؟", Arrays.asList("الفيل", "الزرافة", "الحصان", "الثور"), "الفيل"));
        questions.add(new Question("ما اسم النهر الذي يمر عبر القاهرة؟", Arrays.asList("النيل", "الفرات", "دجلة", "الأمازون"), "النيل"));
        questions.add(new Question("ما هي عاصمة العراق؟", Arrays.asList("بغداد", "بصرى", "دمشق", "الكويت"), "بغداد"));
        questions.add(new Question("ما اسم السورة التي نزلت في غار حراء؟", Arrays.asList("العلق", "الفاتحة", "الكهف", "القدر"), "العلق"));
    }

    void loadProgress() {
        currentQIndex = prefs.getInt("current_q_index", 0);
        score = prefs.getInt("score", 0);
        hintsLeft = prefs.getInt("hints_left", totalHints);
        attemptsLeft = prefs.getInt("attempts_left", attemptsPerQuestion);

        String orderStr = prefs.getString("questions_order", null);
        if (orderStr == null) {
            questionsOrder = new ArrayList<>();
            for (int i = 0; i < questions.size(); i++) questionsOrder.add(i);
            Collections.shuffle(questionsOrder);
        } else {
            questionsOrder = new ArrayList<>();
            String[] parts = orderStr.split(",");
            for (String s : parts) questionsOrder.add(Integer.parseInt(s));
        }
    }

    void saveProgress() {
        SharedPreferences.Editor editor = prefs.edit();
        editor.putInt("current_q_index", currentQIndex);
        editor.putInt("score", score);
        editor.putInt("hints_left", hintsLeft);
        editor.putInt("attempts_left", attemptsLeft);

        StringBuilder sb = new StringBuilder();
        for (int i : questionsOrder) sb.append(i).append(",");
        if (sb.length() > 0) sb.deleteCharAt(sb.length() - 1);
        editor.putString("questions_order", sb.toString());

        editor.apply();
        Toast.makeText(this, "تم حفظ اللعبة", Toast.LENGTH_SHORT).show();
    }

    void setListeners() {
        for (int i = 0; i < 4; i++) {
            final int idx = i;
            optionButtons[i].setOnClickListener(v -> checkAnswer(idx));
        }
        btnHint.setOnClickListener(v -> useHint());
        btnSave.setOnClickListener(v -> saveProgress());
        btnQuit.setOnClickListener(v -> quitGame());
    }

    void showQuestion() {
        if (currentQIndex >= questions.size()) {
            endGame();
            return;
        }
        int qIdx = questionsOrder.get(currentQIndex);
        Question q = questions.get(qIdx);

        tvQuestion.setText("السؤال " + (currentQIndex + 1) + ": " + q.q);

        // خلط خيارات الإجابة
        List<String> opts = new ArrayList<>(q.options);
        Collections.shuffle(opts);

        // تعيين نص الأزرار وإعادة تفعيلها
        for (int i = 0; i < 4; i++) {
            optionButtons[i].setText(opts.get(i));
            optionButtons[i].setEnabled(true);
            optionButtons[i].setBackgroundColor(Color.LTGRAY);
        }

        attemptsLeft = attemptsLeft == 0 ? attemptsPerQuestion : attemptsLeft;
        updateStatus();
    }

    void checkAnswer(int idx) {
        String selected = optionButtons[idx].getText().toString();
        int qIdx = questionsOrder.get(currentQIndex);
        Question q = questions.get(qIdx);

        if (selected.equals(q.answer)) {
            optionButtons[idx].setBackgroundColor(Color.GREEN);
            score++;
            currentQIndex++;
            attemptsLeft = attemptsPerQuestion;
            saveProgress();
            new Handler().postDelayed(this::showQuestion, 1000);
        } else {
            optionButtons[idx].setBackgroundColor(Color.RED);
            optionButtons[idx].setEnabled(false);
            attemptsLeft--;
            updateStatus();
            saveProgress();

            if (attemptsLeft == 0) {
                new AlertDialog.Builder(this)
                        .setTitle("خطأ")
                        .setMessage("انتهت محاولاتك لهذا السؤال، سيتم الانتقال للسؤال التالي.")
                        .setPositiveButton("حسناً", (dialog, which) -> {
                            currentQIndex++;
                            attemptsLeft = attemptsPerQuestion;
                            showQuestion();
                        }).setCancelable(false).show();
            }
        }
    }

    void useHint() {
        if (hintsLeft == 0) {
            Toast.makeText(this, "انتهت التلميحات لديك.", Toast.LENGTH_SHORT).show();
            return;
        }

        int qIdx = questionsOrder.get(currentQIndex);
        Question q = questions.get(qIdx);

        List<Button> wrongButtons = new ArrayList<>();
        for (Button btn : optionButtons) {
            if (!btn.getText().toString().equals(q.answer) && btn.isEnabled()) {
                wrongButtons.add(btn);
            }
        }

        if (wrongButtons.size() <= 1) {
            Toast.makeText(this, "لا يمكن استخدام التلميح الآن.", Toast.LENGTH_SHORT).show();
            return;
        }

        Collections.shuffle(wrongButtons);
        wrongButtons.get(0).setEnabled(false);
        wrongButtons.get(0).setBackgroundColor(Color.LTGRAY);
        wrongButtons.get(1).setEnabled(false);
        wrongButtons.get(1).setBackgroundColor(Color.LTGRAY);

        hintsLeft--;
        updateStatus();
        saveProgress();
    }

    void updateStatus() {
        tvStatus.setText("المحاولات المتبقية: " + attemptsLeft + "    التلميحات المتبقية: " + hintsLeft);
    }

    void endGame() {
        new AlertDialog.Builder(this)
                .setTitle("انتهت اللعبة")
                .setMessage("انتهت اللعبة! نتيجتك: " + score + " من " + questions.size())
                .setPositiveButton("إعادة اللعب", (dialog, which) -> {
                    resetGame();
                    showQuestion();
                })
                .setNegativeButton("خروج", (dialog, which) -> finish())
                .setCancelable(false)
                .show();
        prefs.edit().clear().apply();
    }

    void resetGame() {
        score = 0;
        currentQIndex = 0;
        attemptsLeft = attemptsPerQuestion;
        hintsLeft = totalHints;

        questionsOrder = new ArrayList<>();
        for (int i = 0; i < questions.size(); i++) questionsOrder.add(i);
        Collections.shuffle(questionsOrder);

        saveProgress();
    }

    void quitGame() {
        new AlertDialog.Builder(this)
                .setTitle("خروج")
                .setMessage("هل تريد حفظ اللعبة والخروج؟")
                .setPositiveButton("نعم", (dialog, which) -> {
                    saveProgress();
                    finish();
                })
                .setNegativeButton("لا", (dialog, which) -> finish())
                .show();
    }

}
