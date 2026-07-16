import 'package:flutter/material.dart';

class BirthData {
  final String name;
  final String gender;
  final DateTime birthDate;
  final TimeOfDay birthTime;
  final String birthPlace;

  const BirthData({
    required this.name,
    required this.gender,
    required this.birthDate,
    required this.birthTime,
    required this.birthPlace,
  });

  DateTime get birthDateTime {
    return DateTime(
      birthDate.year,
      birthDate.month,
      birthDate.day,
      birthTime.hour,
      birthTime.minute,
    );
  }
}