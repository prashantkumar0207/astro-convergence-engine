import 'package:flutter/material.dart';

import '../models/horoscope_result.dart';

class ResultScreen extends StatelessWidget {
  final String name;
  final String gender;
  final DateTime birthDate;
  final TimeOfDay birthTime;
  final String birthPlace;
  final HoroscopeResult horoscope;

  const ResultScreen({
    super.key,
    required this.name,
    required this.gender,
    required this.birthDate,
    required this.birthTime,
    required this.birthPlace,
    required this.horoscope,
  });

  Widget _planetTile(String title, String value) {
    return Card(
      elevation: 0,
      child: ListTile(
        title: Text(title),
        trailing: Text(
          value,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Horoscope"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            const Text(
              "Horoscope Generated",
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 30),

            Card(
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [

                    Text(
                      name,
                      style: const TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 8),

                    Text(gender),

                    const SizedBox(height: 8),

                    Text(
                      "${birthDate.day}/${birthDate.month}/${birthDate.year}",
                    ),

                    const SizedBox(height: 8),

                    Text(
                      birthTime.format(context),
                    ),

                    const SizedBox(height: 8),

                    Text(birthPlace),

                  ],
                ),
              ),
            ),

            const SizedBox(height: 35),

            const Text(
              "Ascendant",
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),

            Card(
              child: ListTile(
                title: const Text("Lagna"),
                trailing: Text(
                  horoscope.ascendant,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 30),

            const Text(
              "Planet Positions",
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 12),

            _planetTile("☉ Sun", horoscope.sun),
            _planetTile("☽ Moon", horoscope.moon),
            _planetTile("☿ Mercury", horoscope.mercury),

            const SizedBox(height: 40),

            const Center(
              child: Text(
                "Powered by Astro Convergence Engine",
                style: TextStyle(
                  color: Colors.amber,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),

          ],
        ),
      ),
    );
  }
}