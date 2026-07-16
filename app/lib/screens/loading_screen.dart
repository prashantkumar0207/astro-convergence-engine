import 'package:flutter/material.dart';

import '../models/horoscope_result.dart';
import '../services/horoscope_service.dart';
import 'result_screen.dart';

class LoadingScreen extends StatefulWidget {
  final String name;
  final String gender;
  final DateTime birthDate;
  final TimeOfDay birthTime;
  final String birthPlace;

  const LoadingScreen({
    super.key,
    required this.name,
    required this.gender,
    required this.birthDate,
    required this.birthTime,
    required this.birthPlace,
  });

  @override
  State<LoadingScreen> createState() => _LoadingScreenState();
}

class _LoadingScreenState extends State<LoadingScreen> {
  @override
  void initState() {
    super.initState();
    _generateHoroscope();
  }

  Future<void> _generateHoroscope() async {
    final HoroscopeResult result = await HoroscopeService.generate(
      name: widget.name,
      birthDate: widget.birthDate,
      birthTime: widget.birthTime,
      birthPlace: widget.birthPlace,
      gender: widget.gender,
    );

    if (!mounted) return;

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => ResultScreen(
          name: widget.name,
          gender: widget.gender,
          birthDate: widget.birthDate,
          birthTime: widget.birthTime,
          birthPlace: widget.birthPlace,

          // NEW
          horoscope: result,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(
              width: 70,
              height: 70,
              child: CircularProgressIndicator(
                strokeWidth: 6,
              ),
            ),
            SizedBox(height: 35),
            Text(
              "Calculating Horoscope...",
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 12),
            Text(
              "Running Deterministic Engine",
              style: TextStyle(
                fontSize: 16,
              ),
            ),
          ],
        ),
      ),
    );
  }
}